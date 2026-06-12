#!/usr/bin/env python3
"""Provider-agnostic social image generation helper for Omni Image Studio."""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

ROOT = pathlib.Path(__file__).resolve().parent
SKILL_ROOT = ROOT.parent
PRESETS_PATH = pathlib.Path(os.environ.get("OMNI_IMAGE_PRESETS", str(SKILL_ROOT / "assets" / "platform_presets.json")))
DEFAULT_KEY_PATH = pathlib.Path(os.environ.get("OMNI_IMAGE_API_KEY_FILE", str(SKILL_ROOT / ".secrets" / "image-api-key.txt")))
DEFAULT_OUTPUT_ROOT = pathlib.Path(os.environ.get("OMNI_IMAGE_OUTPUT_ROOT", str(SKILL_ROOT / "outputs" / "images")))
BASE_URL = os.environ.get("OMNI_IMAGE_BASE_URL", "").strip()


def read_key(path: pathlib.Path = DEFAULT_KEY_PATH) -> str:
    env_key = os.environ.get("OMNI_IMAGE_API_KEY", "").strip()
    if env_key:
        return env_key
    if not path.exists():
        raise RuntimeError(
            "Missing API key. Set OMNI_IMAGE_API_KEY or OMNI_IMAGE_API_KEY_FILE. "
            f"Default key file not found: {path}"
        )
    key = path.read_text(encoding="utf-8-sig").strip()
    if not key:
        raise RuntimeError(f"empty API key file: {path}")
    return key


def load_presets() -> Dict[str, Any]:
    return json.loads(PRESETS_PATH.read_text(encoding="utf-8"))


def resolve_preset(platform: str, preset: str) -> Dict[str, Any]:
    data = load_presets()
    try:
        item = data["platforms"][platform]["presets"][preset]
    except KeyError as exc:
        platforms = ", ".join(sorted(data["platforms"].keys()))
        raise SystemExit(f"Unknown preset {platform}/{preset}. Platforms: {platforms}") from exc
    return dict(item)


def http_json(method: str, url: str, api_key: str, payload: Optional[Dict[str, Any]] = None, timeout: int = 120) -> Dict[str, Any]:
    if not BASE_URL:
        raise RuntimeError("Missing OMNI_IMAGE_BASE_URL. Set it to this machine's OpenAI-compatible image API URL, e.g. https://your-provider.example.com/v1")
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            return json.loads(text) if text else {"status": resp.status}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail[:2000]}") from exc


def list_models() -> list[str]:
    data = http_json("GET", BASE_URL.rstrip("/") + "/models", read_key())
    raw = data.get("data", data)
    models = []
    if isinstance(raw, list):
        for item in raw:
            models.append(str(item.get("id") or item.get("model") or item) if isinstance(item, dict) else str(item))
    return models


def make_task_dir(root: pathlib.Path = DEFAULT_OUTPUT_ROOT) -> pathlib.Path:
    out = root / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    return out


def save_b64_image(b64: str, out_path: pathlib.Path) -> pathlib.Path:
    if b64.startswith("data:"):
        b64 = b64.split(",", 1)[1]
    out_path.write_bytes(base64.b64decode(b64))
    return out_path


def extract_and_save_images(response: Dict[str, Any], out_dir: pathlib.Path, base_name: str = "result") -> list[pathlib.Path]:
    saved: list[pathlib.Path] = []
    data = response.get("data")
    if isinstance(data, list):
        for index, item in enumerate(data, 1):
            if not isinstance(item, dict):
                continue
            if item.get("b64_json"):
                saved.append(save_b64_image(item["b64_json"], out_dir / f"{base_name}_{index:02d}.png"))
            elif item.get("url"):
                url = item["url"]
                ext = pathlib.Path(url.split("?", 1)[0]).suffix or ".png"
                path = out_dir / f"{base_name}_{index:02d}{ext}"
                urllib.request.urlretrieve(url, path)
                saved.append(path)
    choices = response.get("choices")
    if isinstance(choices, list):
        for choice_index, choice in enumerate(choices, 1):
            msg = choice.get("message", {}) if isinstance(choice, dict) else {}
            content = msg.get("content")
            if isinstance(content, list):
                for part_index, part in enumerate(content, 1):
                    if not isinstance(part, dict):
                        continue
                    image_url = part.get("image_url") or part.get("url")
                    b64 = part.get("b64_json") or part.get("base64")
                    if isinstance(image_url, dict):
                        image_url = image_url.get("url")
                    if b64:
                        saved.append(save_b64_image(b64, out_dir / f"{base_name}_{choice_index}_{part_index}.png"))
                    elif isinstance(image_url, str) and image_url.startswith("http"):
                        ext = pathlib.Path(image_url.split("?", 1)[0]).suffix or ".png"
                        path = out_dir / f"{base_name}_{choice_index}_{part_index}{ext}"
                        urllib.request.urlretrieve(image_url, path)
                        saved.append(path)
            elif isinstance(content, str):
                (out_dir / f"{base_name}_{choice_index}.txt").write_text(content, encoding="utf-8")
    if not saved:
        (out_dir / "raw_response.json").write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
    return saved


def enhance_prompt(prompt: str, platform: str, preset: str, task_type: str, text: str = "") -> tuple[str, Dict[str, Any]]:
    spec = resolve_preset(platform, preset)
    overlay_rule = ""
    if text:
        overlay_rule = (
            "\nImportant: generate a clean visual background and composition. "
            "Do not render long text inside the AI image; reserve readable empty areas for deterministic text overlay. "
            f"Text to overlay later: {text}"
        )
    full_prompt = (
        f"Create a high-quality {task_type} image for {platform}/{preset}.\n"
        f"Canvas target: {spec['width']}x{spec['height']} px, aspect ratio {spec['ratio']}.\n"
        "Social-media ready composition, strong visual hierarchy, clean margins, no distorted product, no messy text.\n"
        f"User prompt: {prompt}{overlay_rule}"
    )
    return full_prompt, spec


def generate_image(prompt: str, platform: str, preset: str, model: str, task_type: str, text: str = "") -> Dict[str, Any]:
    full_prompt, spec = enhance_prompt(prompt, platform, preset, task_type, text)
    api_key = read_key()
    payload = {"model": model, "prompt": full_prompt, "size": f"{spec['width']}x{spec['height']}", "n": 1, "response_format": "b64_json"}
    try:
        response = http_json("POST", BASE_URL.rstrip("/") + "/images/generations", api_key, payload, timeout=180)
        return {"mode": "images/generations", "prompt": full_prompt, "spec": spec, "response": response}
    except RuntimeError as first_error:
        chat_payload = {"model": model, "messages": [{"role": "user", "content": full_prompt}], "temperature": 0.8, "max_tokens": 2048}
        try:
            response = http_json("POST", BASE_URL.rstrip("/") + "/chat/completions", api_key, chat_payload, timeout=180)
            return {"mode": "chat/completions", "prompt": full_prompt, "spec": spec, "response": response, "first_error": str(first_error)}
        except RuntimeError as second_error:
            return {"mode": "failed", "prompt": full_prompt, "spec": spec, "first_error": str(first_error), "second_error": str(second_error)}


def cmd_list_presets(_: argparse.Namespace) -> int:
    for platform_id, platform_data in load_presets()["platforms"].items():
        print(f"{platform_id} - {platform_data['name']}")
        for preset_id, spec in platform_data["presets"].items():
            print(f"  {preset_id}: {spec['label']} {spec['width']}x{spec['height']} ({spec['ratio']})")
    return 0


def cmd_models(_: argparse.Namespace) -> int:
    for model in list_models():
        print(model)
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    out_dir = make_task_dir()
    result = generate_image(args.prompt, args.platform, args.preset, args.model, args.task_type, args.text or "")
    (out_dir / "task.json").write_text(json.dumps({
        "platform": args.platform,
        "preset": args.preset,
        "model": args.model,
        "task_type": args.task_type,
        "user_prompt": args.prompt,
        "overlay_text": args.text,
        "mode": result.get("mode"),
        "spec": result.get("spec"),
        "first_error": result.get("first_error"),
        "second_error": result.get("second_error"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "prompt.txt").write_text(result.get("prompt", args.prompt), encoding="utf-8")
    saved = extract_and_save_images(result.get("response", {}), out_dir)
    print("out_dir", out_dir)
    print("mode", result.get("mode"))
    for key in ("first_error", "second_error"):
        if result.get(key):
            print(key, result[key][:500])
    for path in saved:
        print("image", path)
    if not saved:
        print("no_image_saved; see raw_response.json/task.json")
        return 2 if result.get("mode") == "failed" else 1
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Omni Image Studio CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("presets").set_defaults(func=cmd_list_presets)
    sub.add_parser("models").set_defaults(func=cmd_models)
    gen = sub.add_parser("generate")
    gen.add_argument("--platform", required=True)
    gen.add_argument("--preset", required=True)
    gen.add_argument("--prompt", required=True)
    gen.add_argument("--text", default="")
    gen.add_argument("--task-type", default="social media image")
    gen.add_argument("--model", default="gpt-image-2")
    gen.set_defaults(func=cmd_generate)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
