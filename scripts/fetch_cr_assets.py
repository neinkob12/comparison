"""Holt die Clash-Royale-Assets fuer die CR-Vergleichsvideos aus den RoyaleAPI-Repos auf GitHub.

Quelle: github.com/RoyaleAPI/cr-api-assets (Bilder, Sounds) und github.com/RoyaleAPI/cr-api-data (Kartendaten).
RoyaleAPI bittet darum, das Repo zu klonen statt die Bilder direkt als CDN zu nutzen, deshalb Sparse-Clone.
Alle Inhalte gehoeren Supercell, Nutzung nur nach der Fan Content Policy (siehe assets/clash_royale/LIZENZ.md).

Ziel: assets/clash_royale/
  cards/<key>.png        alle Karten (Basis, <key>-ev1 = Evolution, <key>-hero = Held), 302x363
  cards.csv              key, Name en/de, Elixier, Seltenheit, Typ, Variante, Datei
  arenas/ chests/ ui/ tokens/ champions/ sfx/ music/
  chr/                   grosse Figuren-Renders (nicht im Repo, nur mit --chr)
Aufruf: python3 scripts/fetch_cr_assets.py [--chr]
"""
import csv, json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "clash_royale"
CACHE = ROOT / ".cache" / "royaleapi"

# Ordner im RoyaleAPI-Repo -> Zielordner
FOLDERS = {
    "cards": "cards", "arenas": "arenas", "chests": "chests", "ui": "ui",
    "trade-tokens": "tokens", "chr_champions": "champions",
}
SFX = [
    "1_cd_02", "2_cd_02", "3_cd_02", "4_cd_02", "5_cd_02", "6_cd_02", "7_cd_02", "8_cd_02", "9_cd_02", "10_cd_02",
    "1st_crown_01", "2nd_crown_01", "3rd_crown_01", "crown_appear_03", "60_sec_warn_02_v2", "big_horn_start_02_v2",
    "card_fly_in_06", "card_ready_02", "card_upgrade_hit_01", "card_upgrade_stat_05", "achievement_unlock_01",
    "buy_common_card_01", "buy_rare_card_01", "buy_epic_card_02", "buy_legnedary_card_01", "button_click_02",
    "deploy_timer_tick_01v4", "bandit_sneaky_laugh_05",
]
MUSIC = ["2min_loop_battle_01", "menu_03"]

# Karten, die in cr-api-data noch fehlen (neu seit 2025). Nur sichere Werte, Rest bleibt leer.
EXTRA = {
    "berserker": (2, "Common", "Troop"), "little-prince": (3, "Champion", "Troop"),
    "goblinstein": (5, "Champion", "Troop"), "boss-bandit": (6, "Champion", "Troop"),
    "goblin-machine": (5, "Legendary", "Troop"), "goblin-demolisher": (4, "Rare", "Troop"),
    "rune-giant": (4, "Epic", "Troop"), "suspicious-bush": (2, "Rare", "Troop"),
    "goblin-curse": (2, "Epic", "Spell"), "void": (3, "Epic", "Spell"), "vines": (3, "Epic", "Spell"),
    "tower-princess": ("", "Common", "Tower"), "cannoneer": ("", "Epic", "Tower"),
    "dagger-duchess": ("", "Legendary", "Tower"), "royal-chef": ("", "Legendary", "Tower"),
}


def clone(repo, paths):
    dest = CACHE / repo
    if not dest.exists():
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse",
                        f"https://github.com/RoyaleAPI/{repo}.git", str(dest)], check=True)
    else:
        subprocess.run(["git", "-C", str(dest), "pull", "-q", "--depth", "1"], check=True)
    subprocess.run(["git", "-C", str(dest), "sparse-checkout", "set", *paths], check=True)
    return dest


def copy_dir(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(src.glob("*.png")):
        shutil.copy2(f, dst / f.name)
        n += 1
    return n


def write_csv(data):
    cards = {c["key"]: c for c in json.loads((data / "docs/json/cards_i18n.json").read_text())}
    rows = []
    for f in sorted((OUT / "cards").glob("*.png")):
        key = f.stem
        if key.startswith("_") or "unknown" in key:
            continue
        variant = "evo" if key.endswith("-ev1") else "base"
        base = key.removesuffix("-ev1")
        if base.endswith("-hero"):
            variant = "hero-evo" if variant == "evo" else "hero"
            base = base.removesuffix("-hero")
        c = cards.get(base)
        if c:
            names = c.get("_lang", {}).get("name", {})
            en, de = c["name"], names.get("de", c["name"])
            elixir, rarity, typ = c["elixir"], c["rarity"], c["type"]
        else:
            en = de = base.replace("-", " ").title()
            elixir, rarity, typ = EXTRA.get(base, ("", "", ""))
        rows.append({"key": key, "base": base, "variant": variant, "name_en": en, "name_de": de,
                     "elixir": elixir, "rarity": rarity, "type": typ, "file": f"cards/{f.name}"})
    with open(OUT / "cards.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def main():
    with_chr = "--chr" in sys.argv
    CACHE.mkdir(parents=True, exist_ok=True)
    paths = list(FOLDERS) + ["LICENSE"] + [f"sfx/{s}.ogg" for s in SFX] + [f"music/{m}.ogg" for m in MUSIC]
    if with_chr:
        paths.append("chr")
    # sparse-checkout set braucht Ordner, einzelne Dateien gehen nur im Nicht-Cone-Modus
    assets = CACHE / "cr-api-assets"
    if not assets.exists():
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout",
                        "https://github.com/RoyaleAPI/cr-api-assets.git", str(assets)], check=True)
    subprocess.run(["git", "-C", str(assets), "sparse-checkout", "set", "--no-cone", *paths], check=True)
    subprocess.run(["git", "-C", str(assets), "checkout", "-q"], check=True)
    data = clone("cr-api-data", ["docs/json"])

    for src, dst in FOLDERS.items():
        print(f"{dst}: {copy_dir(assets / src, OUT / dst)} Bilder")
    if with_chr:
        print(f"chr: {copy_dir(assets / 'chr', OUT / 'chr')} Bilder")
    for kind, names in (("sfx", SFX), ("music", MUSIC)):
        (OUT / kind).mkdir(parents=True, exist_ok=True)
        for n in names:
            shutil.copy2(assets / kind / f"{n}.ogg", OUT / kind / f"{n}.ogg")
    print(f"cards.csv: {write_csv(data)} Karten")


if __name__ == "__main__":
    main()
