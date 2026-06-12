# Omni Image Studio Skill

[![CI](https://github.com/WendyK-LS/omni-image-studio-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/WendyK-LS/omni-image-studio-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://github.com/openclaw/openclaw)

Omni Image Studio is an OpenClaw skill for AI-assisted social media image generation, image workflow routing, and exact-size export across major social, video, and ecommerce platforms.

It is designed for agents that need to generate platform-ready images without hard-coding one provider, one API key, or one machine-specific path.

## Highlights

- Platform presets for Xiaohongshu, Douyin, Bilibili, WeChat, Weibo, Kuaishou, Dewu, Chinese ecommerce, TikTok, Instagram, YouTube, Facebook, Pinterest, X/Twitter, and LinkedIn.
- OpenAI-compatible image generation helper.
- Exact-dimension export helper powered by Pillow.
- Provider-agnostic configuration through environment variables.
- Safer workflow for Chinese text-heavy posters, thumbnails, ecommerce images, and covers.
- OpenClaw-ready `SKILL.md` with reusable operating rules.

## Why this exists

AI image models are great at composition, mood, lighting, and visual concepts, but they are not always reliable at:

- returning exact platform dimensions,
- rendering long Chinese text accurately,
- preserving ecommerce layout constraints,
- producing consistent multi-platform exports.

This skill separates the workflow into two layers:

1. Use the image model for visual generation or clean background creation.
2. Use deterministic local scripts for exact resizing, export, and text-heavy composition workflows.

## Repository Structure

```text
.
├── SKILL.md                      # OpenClaw skill instructions
├── README.md                     # Project documentation
├── assets/
│   └── platform_presets.json     # Platform and size presets
├── examples/
│   └── bilibili-cover.md         # Example workflow
├── scripts/
│   ├── omni_image.py             # Image generation helper
│   └── fit_export.py             # Exact-size export helper
├── requirements.txt
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

## Requirements

- Python 3.10+
- Pillow
- An OpenAI-compatible image API endpoint if you want to use generation

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Set your own image API key and Base URL. This repository does not assume a fixed provider.

```bash
export OMNI_IMAGE_API_KEY="your_image_api_key"
export OMNI_IMAGE_BASE_URL="https://your-openai-compatible-image-api.example.com/v1"
export OMNI_IMAGE_OUTPUT_ROOT="./outputs/images"
```

Alternatively, use an API key file:

```bash
export OMNI_IMAGE_API_KEY_FILE="/path/to/image-api-key.txt"
```

Optional variables:

```bash
export OMNI_IMAGE_PRESETS="./assets/platform_presets.json"
```

PowerShell example:

```powershell
$env:OMNI_IMAGE_API_KEY_FILE = "D:\OpenClaw\.openclaw\secrets\image-api-key.txt"
$env:OMNI_IMAGE_BASE_URL = "https://your-openai-compatible-image-api.example.com/v1"
$env:OMNI_IMAGE_OUTPUT_ROOT = "E:\OpenClaw\.openclaw\workspace\outputs\images"
```

If you use 4sAPI, the Base URL is commonly:

```bash
export OMNI_IMAGE_BASE_URL="https://4sapi.com/v1"
```

## Quick Start

List all supported platform presets:

```bash
python scripts/omni_image.py presets
```

List available models from your configured provider:

```bash
python scripts/omni_image.py models
```

Generate a Bilibili video cover background:

```bash
python scripts/omni_image.py generate \
  --platform bilibili \
  --preset video_cover \
  --task-type "Bilibili video cover" \
  --prompt "futuristic AI entrepreneurship theme, dark blue technology background, empty title area, no text" \
  --text "AI Startup Opportunities" \
  --model gpt-image-2
```

Export a generated image to exact platform dimensions:

```bash
python scripts/fit_export.py outputs/images/example/result_01.png \
  --platform bilibili \
  --preset video_cover \
  --mode cover
```

## Recommended Workflow

1. Identify the platform, preset, content purpose, and final delivery format.
2. Generate a clean visual base with the image model.
3. Avoid asking the model to render long or precise text directly.
4. Add important text with a deterministic local layout step when needed.
5. Export the final image to exact platform dimensions.
6. Inspect the result before delivery.

## Supported Platforms

The preset file currently includes:

- Xiaohongshu
- Douyin
- Bilibili
- WeChat ecosystem
- Weibo
- Kuaishou
- Dewu
- Chinese ecommerce
- TikTok
- Instagram
- YouTube
- Facebook
- Pinterest
- X/Twitter
- LinkedIn

See `assets/platform_presets.json` for exact dimensions.

## OpenClaw Usage

To use this as an OpenClaw skill, install or copy this folder into your OpenClaw skills directory and make sure `SKILL.md` is visible to OpenClaw.

The skill tells the agent to:

- route image tasks through platform presets,
- use provider-specific generation only when configured,
- keep API keys out of public files,
- export exact-size final images,
- inspect outputs before claiming they are ready.

## Security Notes

Never commit:

- API keys,
- `.secrets/`,
- generated outputs,
- customer images or private assets,
- local machine-specific configuration.

The included `.gitignore` excludes common secret and output folders.

## Roadmap

- Add deterministic text overlay templates.
- Add batch export for multiple platforms.
- Add ecommerce white-background helpers.
- Add optional image compression presets.
- Add more example workflows and screenshots.

## Contributing

Contributions are welcome. See `CONTRIBUTING.md`.

## License

MIT License. See `LICENSE`.
