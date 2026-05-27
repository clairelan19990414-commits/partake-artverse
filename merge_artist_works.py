#!/usr/bin/env python3
"""
Merge gallery-scraped works (quiz_artist_works.json) into the main
quiz_images.json. Strategy:
  1. Keep the curated entry (from rebuild_quiz_images.py) as the hero
     because it has a real title + year.
  2. Append the bulk-scraped works as supporting thumbs.
  3. Dedupe by normalized URL.
  4. Cap at 6 works total per artist.
Also fixes the two Wikipedia portrait records that were actually
artwork images (Amy Sillman, Allora & Calzadilla).
"""

import json
import re
from pathlib import Path

DIR = Path(__file__).parent
IMGS = DIR / "quiz_images.json"
SCRAPED = DIR / "quiz_artist_works.json"
PORTRAITS = DIR / "quiz_portraits.json"


def norm(u):
    u = (u or "").split("?")[0]
    u = re.sub(r"\.width-\d+", "", u)
    u = re.sub(r"\.original\b", "", u)
    u = re.sub(r"/_jpg\d+/", "/", u)
    u = re.sub(r"/_webp\d+/", "/", u)
    u = re.sub(r"-\d+x\d+(?=\.\w+$)", "", u)
    return u


def main():
    images = json.loads(IMGS.read_text())
    scraped = json.loads(SCRAPED.read_text())

    for aid, scraped_list in scraped.items():
        if aid not in images:
            continue
        existing = images[aid].get("candidates") or []
        seen = {norm(c["image"]) for c in existing}
        added = 0
        for s in scraped_list:
            n = norm(s["image"])
            if n in seen:
                continue
            seen.add(n)
            existing.append(s)
            added += 1
            if len(existing) >= 6:
                break
        images[aid]["candidates"] = existing[:6]

    IMGS.write_text(json.dumps(images, indent=2, ensure_ascii=False))

    # Strip out two known-bad Wikipedia "portraits" that are actually artworks
    portraits = json.loads(PORTRAITS.read_text())
    for aid in ["a206", "a596"]:  # Sillman -> "Split 2"; Allora -> "Stop Repair Prepare"
        if aid in portraits:
            portraits[aid] = {"url": None, "source": None}
    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))

    # Stats
    counts = {}
    for v in images.values():
        n = len(v.get("candidates", []))
        counts[n] = counts.get(n, 0) + 1
    total_works = sum(len(v.get("candidates", [])) for v in images.values())
    portraits_n = sum(1 for v in portraits.values() if v.get("url"))

    print("Works per artist:")
    for n in sorted(counts):
        print(f"  {n} works: {counts[n]} artists")
    print(f"Total works: {total_works}")
    print(f"Portraits: {portraits_n}/{len(portraits)}")


if __name__ == "__main__":
    main()
