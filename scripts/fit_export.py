#!/usr/bin/env python3
"""Resize/crop an image to exact platform preset dimensions."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent
SKILL_ROOT = ROOT.parent
PRESETS_PATH = pathlib.Path(os.environ.get("OMNI_IMAGE_PRESETS", str(SKILL_ROOT / "assets" / "platform_presets.json")))


def load_spec(platform: str, preset: str):
    data = json.loads(PRESETS_PATH.read_text(encoding="utf-8"))
    return data["platforms"][platform]["presets"][preset]


def fit_export(src: pathlib.Path, dst: pathlib.Path, width: int, height: int, mode: str = "cover"):
    im = Image.open(src).convert("RGB")
    if mode == "cover":
        out = ImageOps.fit(im, (width, height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    elif mode == "contain":
        fitted = ImageOps.contain(im, (width, height), method=Image.Resampling.LANCZOS)
        out = Image.new("RGB", (width, height), (245, 245, 245))
        out.paste(fitted, ((width - fitted.width) // 2, (height - fitted.height) // 2))
    else:
        raise SystemExit("mode must be cover or contain")
    dst.parent.mkdir(parents=True, exist_ok=True)
    suffix = dst.suffix.lower()
    if suffix in (".jpg", ".jpeg"):
        out.save(dst, quality=95, optimize=True)
    else:
        out.save(dst)
    return dst


def main():
    parser = argparse.ArgumentParser(description="Export exact platform dimensions")
    parser.add_argument("src")
    parser.add_argument("--platform", required=True)
    parser.add_argument("--preset", required=True)
    parser.add_argument("--mode", default="cover", choices=["cover", "contain"])
    parser.add_argument("--out")
    args = parser.parse_args()
    src = pathlib.Path(args.src)
    spec = load_spec(args.platform, args.preset)
    out = pathlib.Path(args.out) if args.out else src.with_name(f"{src.stem}_{args.platform}_{args.preset}_{spec['width']}x{spec['height']}.jpg")
    fit_export(src, out, spec["width"], spec["height"], args.mode)
    print(out)


if __name__ == "__main__":
    main()
