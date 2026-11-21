# The World in One Day — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Kleponrachel/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Kleponrachel/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image summing up the world's news of Saturday 21 November 2026:
**48 stories from seven regions** — COP31 spilling into overtime in Antalya,
three Houthi missiles downed over Riyadh, and a 6.7 quake in Peru's Andes
lead the day, with a world map and 16 hotspots, a stories-by-region count
bar, the day in numbers, and 45 more stories in brief.

## How it works

`main.py` (Python 3.13, standard library + Pillow) draws `entry.png`
(1024×1024) deterministically — two runs produce byte-identical output.
It uses only the bundled DejaVu fonts in `fonts/`, so rendering is the
same in any environment. No network access.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Contents

- `main.py` — the program that draws the image
- `entry.png` — the image it produces
- `fonts/` — DejaVu fonts used for rendering (Bitstream Vera license)
- `LICENSE` — MIT
