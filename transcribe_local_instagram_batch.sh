#!/bin/bash
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
VIDEOS="$HOME/Desktop/partake_videos"
HANDLES=(
  aidanetcetera bjornd.al bubsonline codebynordveritas culturalfingerprints
  dan_dug_ davidkylechoe didoriot eugbrandstrat eyes_of_apoorva fakeplasticbrands
  h_miller76 kaburbank lhuijuni.ldn maryisalien musingsofacrouton noteswnat
  thewaronbeauty willfrancis itsvicchang
)
for handle in "${HANDLES[@]}"; do
  if [ ! -d "$VIDEOS/$handle" ]; then
    echo "skip @$handle: no local video folder"
    continue
  fi
  count=$(find "$VIDEOS/$handle" -maxdepth 1 -type f -name '*.mp4' | wc -l | tr -d ' ')
  if [ "$count" = "0" ]; then
    echo "skip @$handle: no mp4 files"
    continue
  fi
  echo "========== @$handle ($count clips) =========="
  "$ROOT/transcribe_instagram_detailed.py" "$handle"
done
