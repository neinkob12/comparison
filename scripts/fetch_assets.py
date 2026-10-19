"""Laedt fehlende Bilder laut assets/manifest.tsv nach assets/<pfad>.jpg.

Manifest-Zeile: <pfad ohne .jpg> TAB <Spotify-Bild-ID (i.scdn.co) oder volle URL>
Aufruf: python3 scripts/fetch_assets.py [--force]
"""
import sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for line in (ROOT / "assets" / "manifest.tsv").read_text(encoding="utf-8").splitlines():
    if "\t" not in line:
        continue
    rel, src = line.split("\t")[:2]
    dst = ROOT / "assets" / f"{rel}.jpg"
    if dst.exists() and "--force" not in sys.argv:
        continue
    url = src if src.startswith("http") else f"https://i.scdn.co/image/{src}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    dst.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    print("geladen:", dst.relative_to(ROOT))
