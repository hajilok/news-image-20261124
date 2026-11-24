[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?ref=41fw6r6c)
[![rank](https://make.fun/badge/news-image-20261124/hajilok/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?ref=41fw6r6c)
[![reward](https://make.fun/badge/news-image-20261124/hajilok/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?ref=41fw6r6c)

# World News Broadsheet — Tuesday, 24 November 2026

Entry for the [make.fun `news-image-20261124` bounty](https://make.fun/bounty/news-image-20261124?ref=41fw6r6c) (*Sum up 24 November's world news in one image*). Join make.fun via [make.fun/r/41fw6r6c](https://make.fun/r/41fw6r6c).

## Overview
- **Entrypoint**: `main.ts` (Node 22, standard library only, zero network calls) deterministically validates and writes `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
- **Format**: Whole PNG/JPEG image (`<= 1024×1024` px, `<= 1 MiB`) designed as an editorial broadsheet summarizing verified primary-source world news from Tuesday, 24 November 2026 across all major global regions and beats.

## Local Verification
```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License
MIT (`LICENSE`).
