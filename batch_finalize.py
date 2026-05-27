#!/usr/bin/env python3
"""
Finalize a batch:
  1. Move processed IDs from queue → completed in quiz_scale_state.json
  2. Update QUIZ_POOL_IDS in artist_map.html with non-red-chip completed IDs
  3. Stage + commit + push to GitHub (Vercel auto-deploys)

Usage: python3 batch_finalize.py
Reads which IDs were just processed by diffing against state.queue —
any queue entries whose IDs now appear in quiz_facts.js are 'done'.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).parent
STATE = DIR / "quiz_scale_state.json"
HTML = DIR / "artist_map.html"
FACTS = DIR / "quiz_facts.js"


def _ids_in_facts():
    src = FACTS.read_text()
    return set(re.findall(r"^  (a\d+):\s*\{", src, re.M))


def _update_pool_array(completed_non_redchip):
    """Replace the QUIZ_POOL_IDS array in artist_map.html with all non-red-chip completed IDs."""
    html = HTML.read_text()
    # Sort by id number for stability
    ids = sorted(completed_non_redchip, key=lambda x: int(x[1:]))
    # Format: chunked into rows of ~12
    rows = []
    for i in range(0, len(ids), 12):
        rows.append("  " + ", ".join(f"'{x}'" for x in ids[i:i+12]))
    new_array = "const QUIZ_POOL_IDS = [\n" + ",\n".join(rows) + "\n];"
    new_html = re.sub(r"const QUIZ_POOL_IDS = \[.*?\];", new_array, html, count=1, flags=re.S)
    HTML.write_text(new_html)


def main():
    state = json.loads(STATE.read_text())
    facts_ids = _ids_in_facts()
    print(f"IDs in quiz_facts.js: {len(facts_ids)}")

    # Move queue items that now have a facts entry → completed
    moved = []
    new_queue = []
    for q in state["queue"]:
        if q["id"] in facts_ids and q["id"] not in state["completed"]:
            state["completed"].append(q["id"])
            moved.append(q["id"])
        elif q["id"] in state["completed"]:
            pass  # already done, drop from queue
        else:
            new_queue.append(q)
    state["queue"] = new_queue
    state["cycle_count"] = state.get("cycle_count", 0) + 1
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    print(f"Moved {len(moved)} IDs queue → completed. New totals: "
          f"{len(state['completed'])} done, {len(state['queue'])} remaining.")

    # Update QUIZ_POOL_IDS — non-red-chip completed only
    red_chip = set(state.get("red_chip_ids", []))
    pool_ids = [aid for aid in state["completed"] if aid not in red_chip]
    _update_pool_array(pool_ids)
    print(f"QUIZ_POOL_IDS updated: {len(pool_ids)} non-red-chip artists in quiz pool.")

    # Git: stage + commit + push
    cycle_n = state["cycle_count"]
    completed_n = len(state["completed"])
    target = state["target_total"]
    files = [
        "artist_map.html", "quiz_facts.js", "quiz_messages.js",
        "quiz_images.json", "quiz_portraits.json", "quiz_scale_state.json",
    ]
    subprocess.run(["git", "-C", str(DIR), "add"] + files, check=True)
    diff = subprocess.run(["git", "-C", str(DIR), "diff", "--cached", "--quiet"]).returncode
    if diff == 0:
        print("No changes to commit.")
        return
    msg = f"quiz: cycle {cycle_n} — {completed_n}/{target} artists ({len(moved)} new)"
    subprocess.run(
        ["git", "-C", str(DIR), "commit", "-m", msg,
         "-m", "Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"],
        check=True)
    push = subprocess.run(["git", "-C", str(DIR), "push", "origin", "HEAD"])
    if push.returncode != 0:
        print("WARN: git push failed — commit is local only.")
    else:
        print(f"Pushed. Cycle {cycle_n} live at Vercel within ~1 min.")


if __name__ == "__main__":
    main()
