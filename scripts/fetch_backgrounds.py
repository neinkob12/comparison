"""Laedt die Natur-Hintergruende fuer die Quiz-Videos (Mixkit, frei nutzbar, keine Namensnennung noetig).

Holt die 4K-Version, schneidet mittig auf Hochformat, 1080x1920, ohne Ton, max. 40 s.
Ziel: video/public/bg/<name>.mp4 (nicht im Repo, zu gross).
Aufruf: python3 scripts/fetch_backgrounds.py [--force]
"""
import subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "video" / "public" / "bg"

# Name -> Mixkit-ID (https://mixkit.co/free-stock-video/...-<id>/)
CLIPS = {
    "wasserfall_sonne": 50564,
    "wasserfall_tropen": 50566,
    "wasserfall_wald": 2213,
    "schlucht": 41401,
    "felsberg_schnee": 51689,
    "waldberge": 41545,
    "alpen": 4132,
    "bergkette": 4366,
    "nebelwald": 22728,
    "nebelberge": 4396,
    "gruenes_panorama": 5360,
    "fluss": 43605,
    "waldweg": 50847,
}

OUT.mkdir(parents=True, exist_ok=True)
for name, mid in CLIPS.items():
    dst = OUT / f"{name}.mp4"
    if dst.exists() and "--force" not in sys.argv:
        continue
    raw = OUT / f"{name}.raw.mp4"
    req = urllib.request.Request(f"https://assets.mixkit.co/videos/{mid}/{mid}-2160.mp4", headers={"User-Agent": "Mozilla/5.0"})
    for i in range(4):
        try:
            raw.write_bytes(urllib.request.urlopen(req, timeout=300).read())
            break
        except Exception:
            if i == 3:
                raise
            time.sleep(2 ** (i + 1))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-t", "40", "-an",
                    "-vf", "crop=ih*9/16:ih,scale=1080:1920,fps=30", "-c:v", "libx264", "-crf", "20",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)], check=True)
    raw.unlink()
    print("geladen:", dst.relative_to(ROOT))
