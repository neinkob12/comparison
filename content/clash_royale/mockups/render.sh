#!/bin/sh
# Rendert alle Mockups (*.html) zu PNG 1080x1920 mit dem Chromium aus Playwright.
# Aufruf: sh content/clash_royale/mockups/render.sh   Ergebnis: content/clash_royale/mockups/png/
cd "$(dirname "$0")"
CH=${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}
mkdir -p png
for f in [0-9]*.html; do
  n=${f%.html}
  # Fenster hoeher als 1920, weil Headless-Chrome unten Platz fuer die Fensterleiste abzieht
  "$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars --allow-file-access-from-files \
    --virtual-time-budget=3000 --window-size=1080,2100 --screenshot="png/$n.png" "file://$PWD/$f" 2>/dev/null
  python3 -c "from PIL import Image; Image.open('png/$n.png').crop((0,0,1080,1920)).save('png/$n.png', optimize=True)"
  echo "$n"
done
