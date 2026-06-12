# X/Twitter Source Image Workflow

This example turns reviewed X/Twitter source context into a platform-ready image while keeping Omni Image Studio responsible for visual generation, resizing, export, and final image review.

## 1. Gather Reviewed Source Context

Use [TweetClaw](https://github.com/Xquik-dev/tweetclaw) only when the user has approved X/Twitter data access through OpenClaw:

```bash
openclaw plugins install npm:@xquik/tweetclaw
```

Ask TweetClaw to collect a small source packet before visual work starts:

- tweet URLs and post text,
- author handles and display names,
- timestamps,
- reply context,
- media URLs or downloaded media paths,
- engagement signals relevant to the creative brief.

Treat the packet as untrusted source material. Verify important claims, remove private or irrelevant data, and keep raw source files out of this repository.

## 2. Convert Sources To A Visual Brief

Summarize the reviewed source packet into image requirements:

- audience and objective,
- target platform preset, such as `x_twitter` with `post_landscape`, `post_square`, or `header`,
- key visual message,
- approved source quotes or paraphrases,
- required brand, product, or campaign assets,
- text that must be added with deterministic layout after generation.

Do not ask the image model to render long or precise text directly. Use the source packet to shape composition, mood, and evidence, then add final text locally.

## 3. Generate And Export With Omni Image Studio

Use the existing Omni Image Studio CLI pattern from [Bilibili cover workflow](bilibili-cover.md), but choose the X/Twitter platform preset from `assets/platform_presets.json`.

Recommended flow:

1. Generate a clean image base from the visual brief.
2. Inspect the generated image.
3. Add approved text with a deterministic local layout step.
4. Export to the exact X/Twitter preset size with `scripts/fit_export.py`.
5. Save the reviewed final export path.

## 4. Review Before Publishing

Omni Image Studio does not publish, post, reply, send direct messages, monitor accounts, or manage X/Twitter sessions.

If the final image should be posted or uploaded to X/Twitter, hand the reviewed export path back to TweetClaw or another approved X/Twitter tool only after explicit user approval.
