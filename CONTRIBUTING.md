# Contributing

Thanks for your interest in improving Omni Image Studio Skill.

## Development Setup

```bash
git clone https://github.com/WendyK-LS/omni-image-studio-skill.git
cd omni-image-studio-skill
python -m pip install -r requirements.txt
```

## Local Checks

Run syntax checks:

```bash
python -m py_compile scripts/omni_image.py scripts/fit_export.py
```

List presets:

```bash
python scripts/omni_image.py presets
```

If you configure an image provider, also test:

```bash
python scripts/omni_image.py models
```

## Pull Request Guidelines

- Do not commit API keys or private customer assets.
- Keep provider-specific behavior configurable through environment variables.
- Add or update examples when adding new workflows.
- Keep `assets/platform_presets.json` valid JSON.
- Prefer exact platform dimensions over approximate ratios.

## Adding Platform Presets

Add new platforms or presets in `assets/platform_presets.json` with this shape:

```json
{
  "label": "Human readable name",
  "width": 1080,
  "height": 1920,
  "ratio": "9:16"
}
```

Use official platform documentation when available. If a platform has multiple valid sizes, prefer the most common creator-friendly size.
