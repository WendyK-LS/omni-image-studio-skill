---
name: omni-image-studio
description: "Generate, edit, resize, and export social media images across major platforms."
---

# Omni Image Studio

Use this skill when the user asks for image generation, image editing, product images, social media covers, ecommerce images, posters, thumbnails, long images, resizing, compression, batch export, or platform-specific image formats.

## What this skill does

- Routes image tasks through a reusable image workflow.
- Chooses platform presets for 小红书, 抖音, B站, 微信, 微博, 快手, 得物, Chinese ecommerce, TikTok, Instagram, YouTube, Facebook, Pinterest, X/Twitter, LinkedIn.
- Uses AI image generation/editing when configured.
- Uses deterministic local resizing/export for exact platform dimensions.
- Avoids asking image models to render long Chinese text; text-heavy designs should be composed locally after generating a clean background.

## Required setup

The helper scripts are in `scripts/` and require Python 3.10+.

Install dependencies:

```bash
python -m pip install pillow
```

Configure one of these before using generation:

```bash
# Option A: API key directly
export OMNI_IMAGE_API_KEY="your_api_key"

# Option B: API key file
export OMNI_IMAGE_API_KEY_FILE="/path/to/image-api-key.txt"
```

Optional configuration:

```bash
export OMNI_IMAGE_BASE_URL="https://your-openai-compatible-image-api.example.com/v1"
export OMNI_IMAGE_OUTPUT_ROOT="./outputs/images"
export OMNI_IMAGE_PRESETS="./assets/platform_presets.json"
```

`OMNI_IMAGE_BASE_URL` must be set to the target machine's own OpenAI-compatible image API URL. Deployments should not assume a fixed provider URL.

On Windows PowerShell:

```powershell
$env:OMNI_IMAGE_API_KEY_FILE = "D:\OpenClaw\.openclaw\secrets\image-api-key.txt"
$env:OMNI_IMAGE_BASE_URL = "https://your-openai-compatible-image-api.example.com/v1"
$env:OMNI_IMAGE_OUTPUT_ROOT = "E:\OpenClaw\.openclaw\workspace\outputs\images"
```

## Workflow

1. Identify the image purpose, target platform, preset, required text, asset inputs, and delivery format.
2. Select a preset from `assets/platform_presets.json`.
3. Choose the pipeline:
   - **Pure generation:** prompt -> image model -> inspect -> exact export.
   - **Product/commercial:** user asset -> generate/edit scene -> deterministic overlay -> inspect.
   - **Text-heavy poster/cover:** generate clean background -> local HTML/SVG/Canvas/Python text composition -> exact export.
   - **Multi-platform export:** make a master design -> export to selected presets.
4. Save outputs under `OMNI_IMAGE_OUTPUT_ROOT`.
5. Preserve `task.json`, `prompt.txt`, raw responses, and final exports.
6. Inspect generated images before final delivery.
7. Final reply should include full paths and attach images when supported.

## CLI examples

List presets:

```bash
python scripts/omni_image.py presets
```

List models:

```bash
python scripts/omni_image.py models
```

Generate a Bilibili cover:

```bash
python scripts/omni_image.py generate \
  --platform bilibili \
  --preset video_cover \
  --task-type "B站视频封面" \
  --prompt "futuristic AI entrepreneurship theme, dark blue technology background, empty title area, no text" \
  --text "AI创业机会" \
  --model gpt-image-2
```

Export exact platform dimensions:

```bash
python scripts/fit_export.py outputs/images/20260612-173852/result_01.png \
  --platform bilibili \
  --preset video_cover \
  --mode cover
```

## Quality rules

- Do not leak API keys.
- Do not hard-code user-specific paths in public releases.
- Do not rely on image models for long Chinese text rendering.
- Always export to exact platform dimensions before delivery.
- Always inspect outputs before claiming they are ready.
- Do not claim ecommerce/legal/platform compliance without human review.

## Provider notes

This skill is provider-agnostic if the provider supports OpenAI-compatible endpoints:

- `GET /models`
- `POST /images/generations`
- optional fallback: `POST /chat/completions`

Provider/model configuration example:

- Base URL: set by `OMNI_IMAGE_BASE_URL`
- model: set with the `--model` argument, for example `gpt-image-2` when supported by your provider

For each machine, replace the Base URL and model name with that machine's own compatible image provider values.
