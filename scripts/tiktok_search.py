"""TikTok-Suche ueber Apify (Actor clockworks/tiktok-scraper, https://apify.com/clockworks/tiktok-scraper).

Key: Umgebungsvariable APIFY_TOKEN (https://console.apify.com/settings/integrations). Netzwerk: api.apify.com.
Ergebnisse landen als JSON in out/tiktok/, kurze Tabelle (nach Views sortiert) auf der Konsole.

  python3 scripts/tiktok_search.py search "wer würdest du eher" -n 30   # Suchbegriff
  python3 scripts/tiktok_search.py search "geld fakten" --sort MOST_LIKED --since PAST_MONTH
  python3 scripts/tiktok_search.py hashtag wuerdestdueher -n 50          # Hashtag (ohne #)
  python3 scripts/tiktok_search.py profile some_creator -n 20            # Videos eines Accounts
  python3 scripts/tiktok_search.py video https://www.tiktok.com/@x/video/123   # einzelne Videos
"""
import argparse, json, os, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "tiktok"
ACTOR = "clockworks~tiktok-scraper"


def run(inp):
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("APIFY_TOKEN fehlt in der Umgebung (neue Session noetig, nachdem er eingetragen wurde).")
    url = f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items?format=json"
    req = urllib.request.Request(url, data=json.dumps(inp).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        # Laeuft synchron, Apify bricht nach 300 s ab
        with urllib.request.urlopen(req, timeout=320) as r:
            return json.loads(r.read() or b"[]")
    except urllib.error.HTTPError as e:
        sys.exit(f"Apify -> {e.code}: {e.read().decode()[:500]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["search", "hashtag", "profile", "video"])
    ap.add_argument("terms", nargs="+")
    ap.add_argument("-n", type=int, default=20, help="Ergebnisse pro Begriff")
    ap.add_argument("--sort", default="MOST_RELEVANT", choices=["MOST_RELEVANT", "MOST_LIKED", "LATEST"])
    ap.add_argument("--since", default="ALL_TIME", choices=["ALL_TIME", "PAST_24_HOURS", "PAST_WEEK", "PAST_MONTH",
                                                             "LAST_3_MONTHS", "LAST_6_MONTHS"])
    ap.add_argument("--download", action="store_true", help="Videos als MP4 im Apify-Speicher ablegen")
    a = ap.parse_args()

    inp = {"resultsPerPage": a.n, "shouldDownloadVideos": a.download, "shouldDownloadCovers": False,
           "downloadSubtitlesOptions": "NEVER_DOWNLOAD_SUBTITLES"}
    if a.mode == "search":
        inp |= {"searchQueries": a.terms, "searchSection": "/video", "videoSearchSorting": a.sort,
                "videoSearchDateFilter": a.since}
    elif a.mode == "hashtag":
        inp["hashtags"] = [t.lstrip("#") for t in a.terms]
    elif a.mode == "profile":
        inp["profiles"] = [t.lstrip("@") for t in a.terms]
    else:
        inp["postURLs"] = a.terms

    items = [i for i in run(inp) if i.get("webVideoUrl")]
    OUT.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "_", "_".join(a.terms).lower())[:40].strip("_") or "video"
    f = OUT / f"{a.mode}_{slug}_{time.strftime('%Y%m%d_%H%M')}.json"
    f.write_text(json.dumps(items, ensure_ascii=False, indent=1))

    items.sort(key=lambda i: i.get("playCount") or 0, reverse=True)
    for i in items:
        text = (i.get("text") or "").replace("\n", " ")[:60]
        print(f"{i.get('playCount', 0):>11,}  {i.get('diggCount', 0):>9,}  "
              f"@{(i.get('authorMeta') or {}).get('name', '?'):<20} {text}  {i['webVideoUrl']}")
    print(f"\n{len(items)} Videos (Views, Likes) -> {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
