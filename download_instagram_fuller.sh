#!/bin/bash
set -u
# Download up to N recent Instagram reels for one or more handles, saving by reel ID.
# This complements the detailed transcriber: existing <id>.mp4 files are not duplicated.
# Usage:
#   ./download_instagram_fuller.sh didoriot lhuijuni.ldn
#   LIMIT=40 ./download_instagram_fuller.sh didoriot

eval "$(/opt/homebrew/bin/brew shellenv zsh)" 2>/dev/null || true
LIMIT="${LIMIT:-40}"
if [ "$#" -eq 0 ]; then
  echo "Usage: LIMIT=40 $0 <handle> [handle...]"
  exit 1
fi
for HANDLE in "$@"; do
  SAVE_DIR="$HOME/Desktop/partake_videos/$HANDLE"
  mkdir -p "$SAVE_DIR"
  echo "========== @$HANDLE · downloading up to $LIMIT reels =========="
  yt-dlp \
    --cookies-from-browser chrome \
    --no-overwrites \
    --download-archive "$SAVE_DIR/.downloaded_reels.txt" \
    --output "$SAVE_DIR/%(id)s.%(ext)s" \
    --format "best[ext=mp4]/bestvideo+bestaudio/best" \
    --merge-output-format mp4 \
    --playlist-items "1-$LIMIT" \
    "https://www.instagram.com/$HANDLE/reels/"
  status=$?
  count=$(find "$SAVE_DIR" -maxdepth 1 -type f -name '*.mp4' | wc -l | tr -d ' ')
  echo "@$HANDLE status=$status local_mp4s=$count"
done
