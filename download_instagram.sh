#!/bin/bash

# ── Partake · Instagram Profile Downloader ────────────────
# Downloads all Reels from an Instagram account.
# Saves to: ~/Desktop/partake_videos/<handle>/
# Requires: yt-dlp, Chrome logged into Instagram

eval "$(/opt/homebrew/bin/brew shellenv zsh)"

clear
echo ""
echo "  +---------------------------------------+"
echo "  |  partake · instagram batch downloader |"
echo "  +---------------------------------------+"
echo ""
echo "  Enter Instagram handle (without @):"
echo ""
read -p "  > " HANDLE

if [ -z "$HANDLE" ]; then
  echo "  No handle entered. Exiting."
  exit 1
fi

SAVE_DIR="$HOME/Desktop/partake_videos/$HANDLE"
mkdir -p "$SAVE_DIR"

echo ""
echo "  Downloading all Reels from @$HANDLE..."
echo "  Saving to: $SAVE_DIR"
echo ""

yt-dlp \
  --cookies-from-browser chrome \
  --output "$SAVE_DIR/%(upload_date)s_%(id)s.%(ext)s" \
  --format "best[ext=mp4]/bestvideo+bestaudio/best" \
  --merge-output-format mp4 \
  --playlist-items 1-60 \
  "https://www.instagram.com/$HANDLE/reels/"

STATUS=$?

echo ""
if [ $STATUS -eq 0 ]; then
  COUNT=$(ls "$SAVE_DIR"/*.mp4 2>/dev/null | wc -l | tr -d ' ')
  echo "  ✓ Done! $COUNT videos saved to $SAVE_DIR"
  echo ""
  echo "  Next: run transcribe_instagram.sh $HANDLE"
  open "$SAVE_DIR"
else
  echo "  Something went wrong. Check that:"
  echo "  · You are logged into Instagram in Chrome"
  echo "  · The account is public or you follow it"
  echo "  · yt-dlp is up to date (brew upgrade yt-dlp)"
fi

echo ""
read -p "  Press Enter to close..."
