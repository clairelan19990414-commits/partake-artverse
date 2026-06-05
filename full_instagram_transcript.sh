#!/usr/bin/env bash
set -euo pipefail

HANDLE="${1:-}"
LIMIT="${2:-60}"
SKIP_TRANSCRIBE="${PARTAKE_SKIP_TRANSCRIBE:-0}"

if [[ -z "$HANDLE" ]]; then
  echo "Usage: $0 <instagram_handle> [limit]" >&2
  echo "Set PARTAKE_SKIP_TRANSCRIBE=1 to download and report coverage without re-transcribing." >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")" && pwd)"
CAPTIONS="$ROOT/transcripts/${HANDLE}_captions.txt"

mkdir -p "$ROOT/transcripts"

if [[ ! -s "$CAPTIONS" ]]; then
  echo "==> Harvesting caption inventory for @$HANDLE ($LIMIT reels)"
  yt-dlp --cookies-from-browser chrome \
    --print "%(id)s | %(title)s | %(description)s" \
    --playlist-items "1-${LIMIT}" \
    "https://www.instagram.com/${HANDLE}/reels/" \
    > "$CAPTIONS"
else
  echo "==> Using existing caption inventory: $CAPTIONS"
fi

echo "==> Downloading videos from caption IDs, not curation IDs"
python3 "$ROOT/download_instagram_ids.py" "$HANDLE" --limit "$LIMIT" --source captions

if [[ "$SKIP_TRANSCRIBE" == "1" ]]; then
  echo "==> Skipping transcription because PARTAKE_SKIP_TRANSCRIBE=1"
else
  echo "==> Transcribing every local mp4 for @$HANDLE"
  python3 "$ROOT/transcribe_instagram_detailed.py" "$HANDLE" \
    --force \
    --model "${PARTAKE_WHISPER_MODEL:-small}" \
    --long-clip-seconds "${PARTAKE_LONG_CLIP_SECONDS:-0}"
fi

echo "==> Coverage report"
python3 - "$ROOT" "$HANDLE" "$LIMIT" <<'PY'
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
handle = sys.argv[2]
limit = int(sys.argv[3])
captions = root / "transcripts" / f"{handle}_captions.txt"
videos = Path.home() / "Desktop" / "partake_videos" / handle
detail = root / "transcripts" / f"{handle}_transcript_detailed.json"

ids = []
if captions.exists():
    for line in captions.read_text(errors="ignore").splitlines():
        first = line.split("|", 1)[0].strip()
        if re.match(r"^[A-Za-z0-9_-]{5,}$", first):
            ids.append(first)
        if len(ids) >= limit:
            break

mp4_ids = {p.stem for p in videos.glob("*.mp4")} if videos.exists() else set()
missing = [post_id for post_id in ids if post_id not in mp4_ids]

clip_count = 0
word_count = 0
if detail.exists():
    data = json.loads(detail.read_text())
    clips = data.get("clips", [])
    clip_count = len(clips)
    word_count = sum(len(re.findall(r"\b\w+\b", c.get("text") or "")) for c in clips)

print(f"caption_ids={len(ids)}")
print(f"local_mp4s={len(mp4_ids)}")
print(f"transcribed_clips={clip_count}")
print(f"transcript_words={word_count:,}")
print("missing_ids=" + (", ".join(missing) if missing else "none"))
PY
