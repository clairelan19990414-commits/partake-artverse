#!/usr/bin/env python3
"""
Pick the next batch of artists to enrich. Prints structured context for
each (raw bio, works, gallery, schools, collectors) so the cron-fired
Claude has everything it needs to write a 3-sentence message and a
structured facts entry.

Usage:
  python3 batch_pick.py [N]      # default N=46
Outputs JSON to stdout AND writes /tmp/quiz_batch_current.json.
"""

import json
import re
import sys
from pathlib import Path

DIR = Path(__file__).parent
STATE = DIR / "quiz_scale_state.json"
HTML = DIR / "artist_map.html"
OUT = Path("/tmp/quiz_batch_current.json")

N_DEFAULT = 46


def _parse_artists():
    """Parse the ARTISTS const out of artist_map.html into a dict keyed by id."""
    src = HTML.read_text()
    m = re.search(r"const ARTISTS = \[(.*?)\n\];", src, re.S)
    block = m.group(1)
    entries = re.findall(
        r"\{ id:'(a\d+)', name:'((?:[^'\\]|\\.)*)', dates:'((?:[^'\\]|\\.)*)', "
        r"gallery:'(g\d+)', museums:\[([^\]]*)\], edu:([^,]+), "
        r"collectors:\[([^\]]*)\], works:\[(.*?)\], bio:'((?:[^'\\]|\\.)*)' \}",
        block,
    )
    galleries = dict(re.findall(r"id:'(g\d+)',\s*name:'((?:[^'\\]|\\.)*)'", src))
    schools = {}
    sblock = re.search(r"const SCHOOLS = \{(.*?)\n\};", src, re.S)
    if sblock:
        for em in re.finditer(
            r"(e\d+):\s*\{\s*name:'((?:[^'\\]|\\.)*)',\s*sub:'((?:[^'\\]|\\.)*)'\s*\}",
            sblock.group(1)):
            schools[em.group(1)] = f"{em.group(2)}, {em.group(3)}"
    museums = {}
    mblock = re.search(r"const MUSEUMS = \[(.*?)\n\];", src, re.S)
    if mblock:
        for mm in re.finditer(
            r"id:'(\w+)',\s*name:'((?:[^'\\]|\\.)*)'", mblock.group(1)):
            museums[mm.group(1)] = mm.group(2)
    collectors = {}
    cblock = re.search(r"const COLLECTORS = \{(.*?)\n\};", src, re.S)
    if cblock:
        for cm in re.finditer(r"(c\d+):'((?:[^'\\]|\\.)*)'", cblock.group(1)):
            collectors[cm.group(1)] = cm.group(2)

    out = {}
    for aid, name, dates, gid, mus_ids, edu, col_ids, works, bio in entries:
        work_list = []
        for wm in re.finditer(r"\{\s*t:'((?:[^'\\]|\\.)*)'(?:,\s*y:'((?:[^'\\]|\\.)*)')?", works):
            work_list.append({"title": wm.group(1).replace("\\'", "'"), "year": wm.group(2) or ""})
        out[aid] = {
            "id": aid,
            "name": name.replace("\\'", "'"),
            "dates": dates,
            "gallery": galleries.get(gid, gid),
            "museums": [museums.get(m.strip().strip("'"), m) for m in mus_ids.split(",") if m.strip()],
            "school": schools.get(edu.strip().strip("'"), None) if edu.strip() != "null" else None,
            "collectors": [collectors.get(c.strip().strip("'"), c) for c in col_ids.split(",") if c.strip()],
            "works": work_list,
            "bio": bio.replace("\\'", "'"),
        }
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else N_DEFAULT
    state = json.loads(STATE.read_text())
    queue = state["queue"]
    if not queue:
        print(json.dumps({"batch": [], "remaining": 0, "msg": "queue empty"}, indent=2))
        return
    artists_data = _parse_artists()
    picks = queue[:n]
    batch = []
    for q in picks:
        a = artists_data.get(q["id"], {})
        batch.append({
            "id": q["id"],
            "name": a.get("name", q["name"]),
            "dates": a.get("dates", q["dates"]),
            "gallery": a.get("gallery"),
            "museums": a.get("museums", []),
            "school": a.get("school"),
            "collectors": a.get("collectors", []),
            "works": a.get("works", []),
            "bio": a.get("bio", ""),
            "red_chip": q["red_chip"],
        })
    result = {
        "batch_size": len(batch),
        "remaining_after": len(queue) - len(batch),
        "completed_so_far": len(state["completed"]),
        "target": state["target_total"],
        "batch": batch,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
