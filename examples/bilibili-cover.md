# Bilibili Cover Workflow Example

This example creates a Bilibili 16:9 video cover workflow.

## 1. Configure Provider

```bash
export OMNI_IMAGE_API_KEY="your_image_api_key"
export OMNI_IMAGE_BASE_URL="https://your-openai-compatible-image-api.example.com/v1"
export OMNI_IMAGE_OUTPUT_ROOT="./outputs/images"
```

## 2. Generate a Clean Background

```bash
python scripts/omni_image.py generate \
  --platform bilibili \
  --preset video_cover \
  --task-type "Bilibili video cover" \
  --prompt "cinematic dark-blue AI startup background, glowing abstract network, clean empty left-side title area, no text, no watermark" \
  --text "AI Startup Opportunities" \
  --model gpt-image-2
```

## 3. Export Exact Size

```bash
python scripts/fit_export.py outputs/images/<task-dir>/result_01.png \
  --platform bilibili \
  --preset video_cover \
  --mode cover
```

Expected final size: `1920x1080`.

## Notes

For Chinese or text-heavy covers, generate a clean background first and add the final title with a deterministic local layout script. Do not rely on the image model for exact Chinese typography.
