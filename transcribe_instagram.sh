#!/bin/bash

# ── Partake · Instagram Transcription Script ──────────────
# Transcribes all mp4s in a handle's folder, merges into one txt.
# Usage: bash transcribe_instagram.sh <handle>
# Output: transcripts/<handle>_transcript.txt

eval "$(/opt/homebrew/bin/brew shellenv zsh)"

HANDLE="$1"
if [ -z "$HANDLE" ]; then
  echo "Usage: bash transcribe_instagram.sh <handle>"
  exit 1
fi

VIDEO_DIR="$HOME/Desktop/partake_videos/$HANDLE"
TRANSCRIPT_DIR="$(dirname "$0")/transcripts"
OUT="$TRANSCRIPT_DIR/${HANDLE}_transcript.txt"

mkdir -p "$TRANSCRIPT_DIR"
> "$OUT"  # clear/create output file

MP4_FILES=("$VIDEO_DIR"/*.mp4)
COUNT=${#MP4_FILES[@]}

echo ""
echo "  Transcribing $COUNT videos from @$HANDLE..."
echo ""

python3 - "$VIDEO_DIR" "$OUT" <<'PYEOF'
import sys, os, glob
from faster_whisper import WhisperModel

video_dir = sys.argv[1]
out_path = sys.argv[2]

model = WhisperModel('small', device='cpu')
files = sorted(glob.glob(os.path.join(video_dir, '*.mp4')))

with open(out_path, 'w') as f:
    for i, path in enumerate(files):
        fname = os.path.basename(path)
        print(f"  [{i+1}/{len(files)}] {fname}")
        try:
            segments, _ = model.transcribe(path, language='en')
            text = ' '.join(s.text for s in segments).strip()
            if text:
                f.write(f'[{fname}]\n{text}\n\n')
        except Exception as e:
            print(f"    ⚠ skipped: {e}")

print(f"\n  ✓ Transcript saved to: {out_path}")
PYEOF
