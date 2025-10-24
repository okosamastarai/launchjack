#!/usr/bin/env bash
set -euo pipefail
HOOK="${1:-Under 1s WP for photographers}"
BG="${2:-shorts/slides/bg1.png}"
OUT="${3:-shorts/exports_pending/demo.mp4}"
FONTFILE=""; for f in "/System/Library/Fonts/SFNS.ttf" "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" "/usr/share/fonts/truetype/freefont/FreeSans.ttf"; do [ -f "$f" ] && FONTFILE="$f" && break; done
if [ -n "$FONTFILE" ]; then
  DTX="drawtext=fontfile=${FONTFILE}:text='${HOOK}':x=(w-text_w)/2:y=h*0.2:fontsize=48:fontcolor=white:box=1:boxcolor=0x000000AA:boxborderw=12"
else
  DTX="drawtext=text='${HOOK}':x=(w-text_w)/2:y=h*0.2:fontsize=48:fontcolor=white:box=1:boxcolor=0x000000AA:boxborderw=12"
fi
ffmpeg -loop 1 -t 26 -i "$BG" -filter_complex "[0:v]scale=1080:1920,format=yuv420p,${DTX}[v]" -map "[v]" -r 30 -y "$OUT"
echo "Rendered $OUT"
