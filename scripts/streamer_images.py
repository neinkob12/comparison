"""Laedt Profilbilder fuer Kanal B nach assets/streamers/<key>.jpg.

Quelle 1: YouTube-Kanal (og:image, 900px), nur wenn der Kanaltitel zum Namen passt.
Quelle 2: Twitch-Avatar ueber decapi.me (300px), Standard-Avatare werden verworfen.
Quelle 0: THUMB (Ausschnitt aus Video-Thumbnail) oder OVERRIDE (echte Fotos, z. B. Wikimedia Commons, wenn Avatar nur ein Logo ist).
Gefundene URLs landen in assets/streamers.tsv, damit man sieht, woher jedes Bild kommt.
Aufruf: python3 scripts/streamer_images.py [key ...]
"""
import re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "assets" / "streamers"
TSV = ROOT / "assets" / "streamers.tsv"
UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "de"}

# key: (YouTube-Handle, Twitch-Login, Woerter, die im Kanaltitel stehen muessen)
CAST = {
    "papaplatte": ("@Papaplatte", "papaplatte", "papaplatte"),
    "montanablack": ("@MontanaBlack", "montanablack88", "montana"),
    "knossi": ("@Knossi", None, "knossi"),
    "trymacs": ("@Trymacs", "trymacs", "trymacs"),
    "unge": ("@unge", None, "unge"),
    "rewinside": ("@rewinside", "rewinside", "rewinside"),
    "handofblood": ("@HandOfBlood", "handofblood", "handofblood"),
    "gronkh": ("@Gronkh", "gronkh", "gronkh"),
    "eliasn97": ("@EliasN97", "eliasn97", "elias"),
    "sidneyeweka": ("@Sidneyeweka", "sidneyeweka", "sidney"),
    "mckytv": ("@McKyTV", "mckytv", "mcky"),
    "reved": ("@Reved", None, "reved"),
    "timgioh": ("@TimGioh", "timgioh", "timgioh"),
    "rumathra": ("@Rumathra", "rumathra", "rumathra"),
    "zarbex": ("@Zarbex", "zarbex", "zarbex"),
    "noway": ("@NoWay4u", "noway4u_sir", "noway"),
    "tanzverbot": ("@Tanzverbot", "tanzverbot", "tanzverbot"),
    "rezo": ("@rezo", "rezo", "rezo"),
    "unsympathischtv": ("@unsympathischTV", None, "unsympathisch"),
    "inscope21": ("@inscope21", None, "inscope"),
    "letshugo": ("@LetsHugo", None, "hugo"),
    "bastighg": ("@BastiGHG", "bastighg", "basti"),
    "stegi": ("@Stegi", "stegi", "stegi"),
    "shurjoka": ("@Shurjoka", "shurjoka", "shurjoka"),
}

# Avatar ist ein Logo oder Cartoon -> lieber echtes Foto (Commons blockt manche Server mit 429, dann Fallback)
OVERRIDE = {
    "montanablack": "https://upload.wikimedia.org/wikipedia/commons/c/c0/MontanaBlack_MarcelEris_Portrait_April_2024.png",
    "trymacs": "https://upload.wikimedia.org/wikipedia/commons/9/93/Trymacs.png",
    "handofblood": "https://upload.wikimedia.org/wikipedia/commons/7/72/HandOfBlood_%2836738811692%29.jpg",
    "gronkh": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Gronkh_IMG_7985.jpg",
}
# Kein Gesicht auf Avatar/Commons -> Ausschnitt aus einem eigenen YouTube-Thumbnail (Video-ID, ffmpeg-crop)
THUMB = {
    "timgioh": ("UwptDm2xDp4", "520:520:760:50"),
    "mckytv": ("lmPOduvIyw4", "560:560:660:60"),
}
TWITCH_FIRST = {"shurjoka"}  # YouTube-Bild ist gezeichnet, Twitch zeigt das Gesicht
UA_COMMONS = {"User-Agent": "comparison-images/1.0 (privates Videoprojekt)"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20).read().decode("utf-8", "replace")


def youtube(handle, must):
    html = get(f"https://www.youtube.com/{handle}")
    title = re.search(r'<meta property="og:title" content="([^"]*)"', html)
    img = re.search(r'<meta property="og:image" content="([^"]*)"', html)
    if title and img and must in title.group(1).lower().replace(" ", ""):
        return img.group(1)


def twitch(login):
    url = get(f"https://decapi.me/twitch/avatar/{login}").strip()
    if url.startswith("https://") and "user-default-pictures" not in url:
        return url


def main(keys):
    DIR.mkdir(parents=True, exist_ok=True)
    rows = {}
    if TSV.exists():
        rows = {l.split("\t")[0]: l for l in TSV.read_text().splitlines() if l}
    for key in keys:
        yt, tw, must = CAST[key]
        if key in THUMB:
            vid, crop = THUMB[key]
            url = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
            raw = DIR / f"{key}.src"
            raw.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", f"crop={crop}", "-q:v", "2", str(DIR / f"{key}.jpg")], check=True)
            raw.unlink()
            rows[key] = f"{key}\tthumbnail\t{url}"
            print("ok", key, "thumbnail")
            continue
        url, src, data = None, None, None
        if key in OVERRIDE:
            try:
                data = urllib.request.urlopen(urllib.request.Request(OVERRIDE[key], headers=UA_COMMONS), timeout=30).read()
                url, src = OVERRIDE[key], "foto"
            except Exception as e:
                print("  foto blockiert, nehme Avatar:", key, e)
        if not url and key in TWITCH_FIRST:
            url, src = twitch(tw), "twitch"
        if not url:
            try:
                url, src = youtube(yt, must), "youtube"
            except Exception as e:
                print("  youtube fehlgeschlagen:", key, e)
        if not url and tw:
            try:
                url, src = twitch(tw), "twitch"
            except Exception as e:
                print("  twitch fehlgeschlagen:", key, e)
        if not url:
            print("FEHLT", key)
            continue
        raw = DIR / f"{key}.src"
        raw.write_bytes(data or urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", "scale='min(1200,iw)':-2", "-q:v", "2", str(DIR / f"{key}.jpg")], check=True)
        raw.unlink()
        rows[key] = f"{key}\t{src}\t{url}"
        print("ok", key, src)
    TSV.write_text("\n".join(rows[k] for k in sorted(rows)) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:] or list(CAST))
