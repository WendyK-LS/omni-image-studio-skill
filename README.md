# Omni Image Studio Skill

OpenClaw skill for all-platform social media image generation, editing workflow, and exact-size export.

## Features

- Platform presets for 小红书, 抖音, B站, 微信, 微博, 快手, 得物, Chinese ecommerce, TikTok, Instagram, YouTube, Facebook, Pinterest, X/Twitter, LinkedIn.
- OpenAI-compatible image generation helper.
- Exact-size export helper based on Pillow.
- Provider-agnostic environment variables.
- Safe workflow for text-heavy Chinese covers and ecommerce images.

## Install

Copy or install this folder as an OpenClaw skill.

Install Python dependency:

```bash
python -m pip install pillow
```

Configure an OpenAI-compatible image API. Use the target machine's own Base URL and API key:

```bash
export OMNI_IMAGE_API_KEY="your_image_api_key"
export OMNI_IMAGE_BASE_URL="https://your-openai-compatible-image-api.example.com/v1"
export OMNI_IMAGE_OUTPUT_ROOT="./outputs/images"
```

If you use 4sAPI, the Base URL is usually:

```bash
export OMNI_IMAGE_BASE_URL="https://4sapi.com/v1"
```

Windows PowerShell example:

```powershell
$env:OMNI_IMAGE_API_KEY_FILE = "D:\OpenClaw\.openclaw\secrets\image-api-key.txt"
$env:OMNI_IMAGE_BASE_URL = "https://your-openai-compatible-image-api.example.com/v1"
$env:OMNI_IMAGE_OUTPUT_ROOT = "E:\OpenClaw\.openclaw\workspace\outputs\images"
```

## Usage

```bash
python scripts/omni_image.py presets
python scripts/omni_image.py models
python scripts/omni_image.py generate --platform bilibili --preset video_cover --prompt "futuristic AI cover, no text" --text "AI创业机会"
python scripts/fit_export.py outputs/images/example/result_01.png --platform bilibili --preset video_cover --mode cover
```

## Publish notes

Do not commit API keys, generated outputs, `.secrets/`, or local customer assets.

Recommended GitHub/UUMIT package contents:

- `SKILL.md`
- `README.md`
- `assets/platform_presets.json`
- `scripts/omni_image.py`
- `scripts/fit_export.py`
- `.gitignore`
- `requirements.txt`
- `LICENSE`
