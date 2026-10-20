"""Holt die deutschen Auto-Untertitel der Hugo-Kanaele (ab 2023) als Text.

Laeuft auf deinem eigenen PC, weil YouTube Cloud-Server blockt.
Einmalig:  pip install yt-dlp
Starten:   python scripts/hugo_transcripts.py
Falls YouTube "Sign in to confirm you're not a bot" sagt:
           python scripts/hugo_transcripts.py --browser chrome   (oder firefox, edge)

Ergebnis: content/streamer/transcripts/<kanal>/<video-id>.json
  {id, channel, title, date, duration, text, lines: [[sekunde, text], ...]}
Schon geholte Videos werden uebersprungen, du kannst also jederzeit abbrechen und neu starten.
Danach: git add content/streamer/transcripts && git commit -m "Hugo-Transkripte" && git push
"""
import argparse, json, random, sys, time
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp fehlt. Bitte erst ausfuehren:  pip install yt-dlp")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "streamer" / "transcripts"
CHANNELS = {
    "hungrigerhugo": "https://www.youtube.com/@HungrigerHugo/videos",
    "satterhugo": "https://www.youtube.com/@SatterHugo/videos",
}
SINCE = "20230101"
STOP_AFTER_OLD = 15  # Liste ist neu -> alt sortiert, nach so vielen alten Videos am Stueck aufhoeren


def video_ids(ydl, url):
    info = ydl.extract_info(url, download=False, process=False)
    for e in info.get("entries") or []:
        if e and e.get("id"):
            yield e["id"]


def caption_lines(ydl, info):
    tracks = info.get("subtitles", {}).get("de") or info.get("automatic_captions", {}).get("de") \
        or info.get("automatic_captions", {}).get("de-orig")
    if not tracks:
        return None
    url = next((t["url"] for t in tracks if t.get("ext") == "json3"), None)
    if not url:
        return None
    data = json.loads(ydl.urlopen(url).read().decode("utf-8"))
    lines = []
    for ev in data.get("events", []):
        text = "".join(s.get("utf8", "") for s in ev.get("segs") or []).replace("\n", " ").strip()
        if text:
            lines.append([round(ev.get("tStartMs", 0) / 1000), text])
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--browser", help="Cookies aus diesem Browser nehmen (chrome, firefox, edge, ...)")
    ap.add_argument("--max", type=int, default=0, help="hoechstens so viele neue Videos pro Kanal (0 = alle)")
    args = ap.parse_args()

    opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    if args.browser:
        opts["cookiesfrombrowser"] = (args.browser,)
    with yt_dlp.YoutubeDL(opts) as ydl:
        for name, url in CHANNELS.items():
            folder = OUT / name
            folder.mkdir(parents=True, exist_ok=True)
            done, old, new = {p.stem for p in folder.glob("*.json")}, 0, 0
            print(f"\n== {name}")
            for vid in video_ids(ydl, url):
                if vid in done:
                    continue
                try:
                    info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
                except Exception as e:
                    print("  Fehler", vid, str(e)[:120])
                    if "not a bot" in str(e):
                        sys.exit("YouTube will eine Anmeldung. Nochmal starten mit:  --browser chrome")
                    continue
                if (info.get("upload_date") or "0") < SINCE:
                    old += 1
                    if old >= STOP_AFTER_OLD:
                        break
                    continue
                old = 0
                lines = caption_lines(ydl, info)
                if not lines:
                    print("  keine Untertitel", vid, info.get("title", "")[:60])
                    continue
                rec = {"id": vid, "channel": name, "title": info.get("title"), "date": info.get("upload_date"),
                       "duration": info.get("duration"), "views": info.get("view_count"),
                       "text": " ".join(t for _, t in lines), "lines": lines}
                (folder / f"{vid}.json").write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
                new += 1
                print(f"  ok {info.get('upload_date')} {info.get('title', '')[:70]}")
                if args.max and new >= args.max:
                    break
                time.sleep(random.uniform(1.5, 4))  # langsam, damit YouTube nicht blockt
            print(f"   {new} neue Transkripte")
    print("\nFertig. Jetzt pushen:  git add content/streamer/transcripts && git commit -m \"Hugo-Transkripte\" && git push")


if __name__ == "__main__":
    main()
