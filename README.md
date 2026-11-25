[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/itslanaa/news-image-20261125-v3/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/itslanaa/news-image-20261125-v3/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# News Image 20261125 v3 — The World in One Day

Sum up Wednesday 25 November 2026's world news in one image.

An entry for the [news-image-20261125 bounty on make.fun](https://make.fun/bounty/news-image-20261125).

## The image

A one-page front page, 1024×1024, drawn fresh for this day:

- **13 illustrated stories:** Shenzhou-24 launches and docks with the
  first foreign astronaut aboard Tiangong; Trump on Iran, Kim and a
  Zelensky peace deal; 700,000+ Russian soldiers killed; Odesa and Kyiv
  strikes; the CIA breach; the Houthis hitting Ras Tanura and Riyadh;
  ASEAN–China failing on a sea code; a Geran-5 downed; TikTok abuse in
  Israel; a Myanmar quake study. Each has an original drawn scene, a
  number, a place, a certainty badge and a named source.
- **14 more in ALSO ON**, each with a UTC time and a source code
  (C = 2+ outlets, O = official, R = one outlet, CL = one side's claim),
  plus a stats strip, a UTC ticker, a region bar
  and a world map with numbered pins 1–13 matching the stories.
- **27 stories, 8 regions:** every story was verified as first reported
  on Wednesday 25 November 2026 (Reuters, Xinhua, Al Jazeera, RFE/RL,
  NY Post, WSJ and others). A DATE CHECK box lists what was left out
  because it happened on an earlier day.

## How it is built

`draw_frontpage.py` renders `entry.png` with Python PIL and DejaVu fonts
only (with a resilient font fallback). It is deterministic: re-running it
produces byte-identical output.

`main.ts` (Node 22, standard library only) copies the committed
pre-rendered `entry.png` to `/output/entry.png`. It never spawns another
program: the grading container has no Python, so copying the committed
image is the reliable path.

## Run it

```sh
python3 draw_frontpage.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see `LICENSE`.
