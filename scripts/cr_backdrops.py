"""Baut die Hintergruende fuer die CR-Vergleichsvideos (1080x1920) aus den RoyaleAPI-Assets.

Vorher: python3 scripts/fetch_cr_assets.py
Ziel: assets/clash_royale/backdrops/<name>.png
  menu_blue      CR-Menue: blaues Rautenmuster mit Vignette
  arena_split    Arena von oben: Gras-Schachbrett, Fluss mit zwei Bruecken, oben rot, unten blau
  legendary      Lila mit Strahlen (Legendaer-Look)
  gold_rays      Gold mit Strahlen (Truhe oeffnen)
  arena_<name>   Arena-Bild weichgezeichnet und abgedunkelt
Aufruf: python3 scripts/cr_backdrops.py
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
CR = ROOT / "assets" / "clash_royale"
OUT = CR / "backdrops"
W, H = 1080, 1920


def vignette(img, strength=0.75, center=(0.5, 0.45)):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    cx, cy = W * center[0], H * center[1]
    for i in range(60):
        t = i / 59
        r = 1500 * (1 - t) + 350 * t
        d.ellipse((cx - r * 0.75, cy - r, cx + r * 0.75, cy + r), fill=int(255 * strength * (1 - t)))
    mask = mask.filter(ImageFilter.GaussianBlur(80))
    return Image.composite(Image.new("RGB", (W, H), (4, 10, 40)), img, mask)


def menu_blue():
    tile = Image.open(CR / "ui" / "ui-tex-2.png").convert("RGB").resize((300, 300), Image.LANCZOS)
    img = Image.new("RGB", (W, H))
    for x in range(0, W, 300):
        for y in range(0, H, 300):
            img.paste(tile, (x, y))
    return vignette(img, 0.7)


def rays(c1, c2, n=18, center=(W / 2, H * 0.42)):
    img = Image.new("RGB", (W, H), c2)
    d = ImageDraw.Draw(img)
    cx, cy = center
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 0.5) / n
        d.polygon([(cx, cy), (cx + 3000 * math.cos(a0), cy + 3000 * math.sin(a0)),
                   (cx + 3000 * math.cos(a1), cy + 3000 * math.sin(a1))], fill=c1)
    img = img.filter(ImageFilter.GaussianBlur(6))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((cx - 420, cy - 420, cx + 420, cy + 420), fill=200)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.composite(Image.new("RGB", (W, H), (255, 245, 210)), img, glow)
    return vignette(img, 0.6, (0.5, center[1] / H))


def arena_split():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    s = 90  # Kachelgroesse wie im Spiel: helles und dunkles Gras im Wechsel
    for gx in range(0, W, s):
        for gy in range(0, H, s):
            light = (gx // s + gy // s) % 2 == 0
            d.rectangle((gx, gy, gx + s, gy + s), fill=(126, 196, 76) if light else (110, 180, 64))
    # Fluss und Bruecken
    ry = H // 2
    d.rectangle((0, ry - 70, W, ry + 70), fill=(64, 170, 230))
    d.rectangle((0, ry - 70, W, ry - 56), fill=(150, 120, 80))
    d.rectangle((0, ry + 56, W, ry + 70), fill=(150, 120, 80))
    for bx in (200, W - 200):
        d.rounded_rectangle((bx - 80, ry - 100, bx + 80, ry + 100), 12, fill=(176, 128, 74), outline=(110, 74, 40), width=8)
        for k in range(-80, 100, 36):
            d.line((bx - 72, ry + k, bx + 72, ry + k), fill=(140, 96, 52), width=5)
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    # Team-Faerbung: oben rot (Gegner), unten blau (du)
    top = Image.blend(img.crop((0, 0, W, ry)), Image.new("RGB", (W, ry), (230, 40, 60)), 0.14)
    bottom = Image.blend(img.crop((0, ry, W, H)), Image.new("RGB", (W, H - ry), (40, 90, 240)), 0.14)
    img.paste(top, (0, 0))
    img.paste(bottom, (0, ry))
    return vignette(img, 0.3, (0.5, 0.5))


def arena_blur(name):
    a = Image.open(CR / "arenas" / f"{name}.png").convert("RGBA")
    a = a.crop(a.getbbox()).resize((H, H), Image.LANCZOS)
    img = Image.new("RGB", (W, H), (10, 20, 50))
    img.paste(a, ((W - H) // 2, 0), a)
    img = img.filter(ImageFilter.GaussianBlur(28))
    img = Image.blend(img, Image.new("RGB", (W, H), (8, 14, 40)), 0.35)
    return vignette(img, 0.55)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = {
        "menu_blue": menu_blue, "arena_split": arena_split,
        "legendary": lambda: rays((150, 60, 230), (70, 20, 140)),
        "gold_rays": lambda: rays((255, 190, 40), (220, 120, 10)),
    }
    # Arena-Renders, nicht die Liga-Abzeichen (arena14-19, league*)
    for name in ("arena3", "arena7", "arena8", "arena9", "arena12", "legendary"):
        jobs[f"arena_{name.removeprefix('arena')}"] = lambda name=name: arena_blur(name)
    for name, fn in jobs.items():
        fn().save(OUT / f"{name}.png", optimize=True)
        print(name)


if __name__ == "__main__":
    main()
