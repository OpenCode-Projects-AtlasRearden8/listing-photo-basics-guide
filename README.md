# Listing Photo Basics

A small-business manual for **resale listing photos that actually sell** — built on a phone, from a corner of a room, on any budget. For people selling on eBay, Amazon, Etsy, Mercari, Poshmark, or publishing covers via KDP.

Written in the plain, warm, step-by-step style of [Asdale Dynamics, LLC](https://dylanasdale.github.io): clear like a friend explaining, never condescending, always first-practical.

## What's inside

- **The corner lab on any budget** — $0, ~$25, and ~$75 setups; set it up once, reuse forever
- **Light without a rig** — window light, bounce, diffusion, time-of-day habits
- **Honest condition shots that cut disputes** — flaw disclosure buyers trust
- **Backgrounds and scale props** — backdrops plus the ruler/coin/tape habit
- **Before/after cleaning shots** — fairness rules so the pair builds trust, not suspense
- **Phone editing without fakery** — fix the camera's lies; never the item's facts
- **Per-marketplace size habits** — eBay, Amazon, Etsy, KDP cover specs in plain tables
- **Shot-list cards** — copy-and-keep lists for nine item categories
- **A one-page editing checklist** — pre-upload pass and an ADHD-friendly batch plan
- **Glossary** — plain definitions for photography and marketplace vocabulary

The sibling guide *Smartphone Photo Basics* covers family/document photos; this one is for things you sell.

## Quick start

```bash
python3 build.py        # builds site/ from docs/
open site/index.html    # macOS; or just double-click the file
```

Requirements: Python 3 plus the [`markdown`](https://pypi.org/project/markdown/) package (`python3 -m pip install markdown`). Anything else — no network access, no CDNs, no external fonts — the build is fully local-first.

## Repository layout

```
build.py    Build script: docs/*.md -> site/*.html (static, offline)
docs/       The manual as Markdown (the source of truth)
site/       Built static HTML site — regenerate with build.py
```

## Reading offline

Open `site/index.html` directly after building, or read the Markdown in `docs/` in numbered order (index → corner lab → light → condition → backgrounds → cleaning → editing → marketplaces → shot lists → checklist → glossary).

## Platform specs note

Marketplace photo specs in this guide summarize each platform's own public help pages as of late 2026 (eBay, Amazon, Etsy, and Amazon KDP). These rotate occasionally; when they do, the platform's page wins over this manual.

## License and credits

Produced by **Asdale Dynamics, LLC** — beginner-friendly AI education, author and small-business tools, and practical utilities you can publish or sell.

Licensed under the MIT License. See [LICENSE](LICENSE).

**Copyright (c) 2026 Asdale Dynamics, LLC**
