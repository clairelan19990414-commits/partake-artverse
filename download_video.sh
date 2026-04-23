#!/bin/bash

# ── Partake Video Downloader ──────────────────────────────
# Works with: Patreon, Instagram, YouTube, Vimeo, and more
# Double-click this file to run, paste your URL when asked.

eval "$(/opt/homebrew/bin/brew shellenv zsh)"

SAVE_DIR="$HOME/Desktop/partake_videos"
mkdir -p "$SAVE_DIR"

clear
echo ""
echo "  +---------------------------------+"
echo "  |   partake · video downloader   |"
echo "  +---------------------------------+"
echo ""
echo "  Paste the video URL and press Enter:"
echo "  (Patreon, Instagram, YouTube, Vimeo...)"
echo ""
read -p "  > " VIDEO_URL

if [ -z "$VIDEO_URL" ]; then
  echo "  No URL entered. Exiting."
  exit 1
fi

echo ""
echo "  Downloading..."
echo ""

yt-dlp \
  --js-runtimes node \
  --remote-components "ejs:github" \
  --cookies-from-browser chrome \
  --output "$SAVE_DIR/%(title)s.%(ext)s" \
  --format "best[ext=mp4]/bestvideo+bestaudio/best" \
  --merge-output-format mp4 \
  "$VIDEO_URL"

STATUS=$?

echo ""
if [ $STATUS -eq 0 ]; then
  echo "  ✓ Done! File saved to ~/Desktop/partake_videos/"
  echo ""
  open "$SAVE_DIR"
else
  echo "  Something went wrong. Check that:"
  echo "  · You are logged into Patreon/Instagram in Chrome"
  echo "  · The URL is correct and the content is accessible"
fi

echo ""
read -p "  Press Enter to close..."
