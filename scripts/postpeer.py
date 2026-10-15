"""TikTok-Upload ueber PostPeer (https://www.postpeer.dev/docs).

Key: Umgebungsvariable POSTPEER_API_KEY. Netzwerk: api.postpeer.dev, assets.postpeer.dev, *.amazonaws.com (Upload-URL).

  python3 scripts/postpeer.py accounts
  python3 scripts/postpeer.py draft   a49                 # als Entwurf ins TikTok-Postfach
  python3 scripts/postpeer.py private a50                 # direkt posten, nur fuer dich sichtbar (Test)
  python3 scripts/postpeer.py schedule a07 2026-10-16T12:30:00   # oeffentlich zur Uhrzeit (Europe/Berlin)
  python3 scripts/postpeer.py plan a15 a50 [--draft]      # alle laut docs/posting_plan.csv einplanen
"""
import csv, json, os, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.postpeer.dev/v1"
TZ = "Europe/Berlin"


def call(method, path, body=None):
    key = os.environ.get("POSTPEER_API_KEY")
    if not key:
        sys.exit("POSTPEER_API_KEY fehlt in der Umgebung (neue Session noetig, nachdem er eingetragen wurde).")
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"x-access-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> {e.code}: {e.read().decode()[:500]}")


def tiktok_account():
    data = call("GET", "/connect/integrations")
    items = data.get("data") or data.get("integrations") or data
    for it in items if isinstance(items, list) else []:
        if str(it.get("platform", "")).lower() == "tiktok":
            return it.get("accountId") or it.get("id")
    sys.exit(f"Kein verbundener TikTok-Account gefunden: {json.dumps(data)[:400]}")


def upload(vid):
    f = ROOT / "out" / "cut" / f"{vid}.mp4"
    up = call("POST", "/media/upload", {"filename": f.name, "mimeType": "video/mp4"})["data"]
    req = urllib.request.Request(up["uploadUrl"], method="PUT", data=f.read_bytes(), headers={"Content-Type": "video/mp4"})
    urllib.request.urlopen(req, timeout=300).read()
    return up["publicUrl"]


def caption(vid):
    for r in csv.DictReader(open(ROOT / "docs" / "posting_plan.csv")):
        if r["datei"] == f"{vid}.mp4":
            return r
    sys.exit(f"{vid} nicht im Posting-Plan")


def post(vid, mode, when=None):
    acc = tiktok_account()
    row = caption(vid)
    psd = {"privacyLevel": "SELF_ONLY" if mode == "private" else "PUBLIC_TO_EVERYONE", "isAigc": True}
    if mode == "draft":
        psd["draft"] = True
    body = {"content": row["caption"], "platforms": [{"platform": "tiktok", "accountId": acc, "platformSpecificData": psd}],
            "mediaItems": [{"type": "video", "url": upload(vid)}]}
    if when:
        body.update({"scheduledFor": when, "timezone": TZ})
    else:
        body["publishNow"] = True
    res = call("POST", "/posts", body)
    print(vid, mode, when or "jetzt", json.dumps(res, ensure_ascii=False)[:400])
    return res


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "accounts":
        print(json.dumps(call("GET", "/connect/integrations"), indent=1, ensure_ascii=False))
    elif cmd in ("draft", "private"):
        post(args[0], cmd)
    elif cmd == "schedule":
        post(args[0], "public", args[1])
    elif cmd == "plan":
        a, b = int(args[0][1:]), int(args[1][1:])
        mode = "draft" if "--draft" in args else "public"
        for n in range(a, b + 1):
            r = caption(f"a{n:02d}")
            post(f"a{n:02d}", mode, f"{r['datum']}T{r['uhrzeit']}:00")
