# Security Policy

## Supported Versions

This project is currently early-stage. Security fixes are applied to the latest `main` or `master` branch.

## Reporting a Vulnerability

If you discover a vulnerability, please open a GitHub issue with a minimal description and avoid including secrets, API keys, customer data, or private image assets.

## Secret Handling

This project must never include:

- API keys,
- provider tokens,
- `.secrets/` directories,
- generated customer outputs,
- local machine-specific credentials,
- private image assets.

Use environment variables instead:

```bash
export OMNI_IMAGE_API_KEY="your_image_api_key"
export OMNI_IMAGE_BASE_URL="https://your-provider.example.com/v1"
```

Or use a local key file excluded from Git:

```bash
export OMNI_IMAGE_API_KEY_FILE="/path/to/local/key.txt"
```

## Provider Trust

The scripts send prompts to the configured image provider. Only use providers you trust with your prompt and asset data.
