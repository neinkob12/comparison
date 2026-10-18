"""TikTok-Upload kostenlos ueber den Browser (haziq-exe/TikTokAutoUploader), mit KI-Kennzeichnung.

Laeuft auf deinem eigenen Rechner (Heim-Internet), NICHT in der Cloud.

Einmalig installieren:
  pip install tiktokautouploader
  phantomwright_driver install chromium
  (Node.js muss installiert sein)

Benutzung (aus dem Repo-Ordner):
  python3 scripts/tiktok_upload.py shift a17 2026-10-19       # Plan ab a17 neu datieren, 4 pro Tag ab diesem Datum
  python3 scripts/tiktok_upload.py test a17                   # 1 Video als Entwurf, Browser sichtbar
  python3 scripts/tiktok_upload.py plan a17 a24               # einplanen laut docs/posting_plan.csv
  python3 scripts/tiktok_upload.py plan a17 a24 --draft       # nur als Entwurf speichern
  python3 scripts/tiktok_upload.py inspect a17                # postet nichts, speichert Sound-/Cover-Ansicht nach out/debug/

Optionen:
  --at "JJJJ-MM-TT HH:MM"  andere Uhrzeit als im Plan (Minuten in 5er-Schritten), z.B. fuer Tests
  --account NAME   gespeicherte Sitzung waehlen (Standard: ACCOUNT unten), pro Konto eigener Login
  --sound NAME     Name des Sounds in deinen TikTok-Favoriten (Standard: SOUND unten)
  --manual-ai      vor jedem Absenden anhalten, du setzt den KI-Haken selbst und drueckst Enter
  --headless       Browser unsichtbar (erst nutzen, wenn die Tests sauber laufen)

Beim ersten Start oeffnet sich ein Login-Fenster. Danach liegt die Sitzung in TK_cookies_<konto>.json
(wie ein Passwort behandeln, ist in .gitignore).
"""
import csv, datetime as dt, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "docs" / "posting_plan.csv"
ACCOUNT = "finanzen_einfach"  # nur Name der gespeicherten Sitzung, gepostet wird auf das Konto, mit dem du dich einloggst
SOUND = "Solitude"  # Stichwort reicht: haziq nimmt den ersten Favoriten, der alle Woerter enthaelt
TIMES = ["12:30", "16:00", "18:30", "21:00"]
AI_TEXT = re.compile(r"AI[- ]generated content|KI-generierte", re.I)


def rows():
    return list(csv.DictReader(open(PLAN, encoding="utf-8")))


def num(vid):
    return int(vid.lstrip("a"))


def shift(start_vid, start_date):
    rs, day, slot = rows(), dt.date.fromisoformat(start_date), 0
    for r in rs:
        if num(r["datei"][:-4]) >= num(start_vid):
            r["datum"], r["uhrzeit"] = day.isoformat(), TIMES[slot]
            slot = (slot + 1) % len(TIMES)
            day += dt.timedelta(days=slot == 0)
    with open(PLAN, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rs[0].keys())
        w.writeheader()
        w.writerows(rs)
    print(f"Plan ab {start_vid} startet jetzt am {start_date}, letztes Video: {rs[-1]['datum']} {rs[-1]['uhrzeit']}")


def split_caption(caption):
    tags = re.findall(r"#\S+", caption)
    text = re.sub(r"\s*#\S+", "", caption).strip()
    return text, tags


def set_ai_label(page):
    """Schaltet 'AI-generated content' ein. Gibt True zurueck, wenn der Schalter sicher an ist."""
    for label in ("Show more", "Mehr anzeigen"):
        more = page.get_by_text(label, exact=True)
        if more.count() and more.first.is_visible():
            more.first.click()
            time.sleep(1)
            break
    row = page.locator('[data-e2e="aigc_container"]')
    if not row.count():
        row = page.locator("div", has_text=AI_TEXT).filter(
            has=page.locator('[role="switch"], input[type="checkbox"], [data-part="thumb"]')).last
    if not row.count():
        return False
    row.scroll_into_view_if_needed()
    if not is_on(row):
        row.locator('[data-part="thumb"], [role="switch"], input[type="checkbox"]').first.click(force=True)
        time.sleep(1)
        for btn in ("Turn on", "Einschalten", "Confirm"):
            b = page.locator(f'button:has-text("{btn}")')
            if b.count() and b.first.is_visible():
                b.first.click()
                time.sleep(1)
                break
    return is_on(row)


def is_on(row):
    box = row.locator('input[type="checkbox"]')
    if box.count():
        return box.first.is_checked()
    sw = row.locator('[role="switch"], [aria-checked], [data-state]')
    if sw.count():
        return (sw.first.get_attribute("aria-checked") == "true"
                or sw.first.get_attribute("data-state") in ("checked", "on"))
    return False


def dump(page, name):
    """Speichert Screenshot + bereinigtes HTML (ohne Scripts/Styles/Icons), damit Selektoren gebaut werden koennen."""
    d = ROOT / "out" / "debug"
    d.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(d / f"{name}.png"), full_page=True)
    html = page.evaluate("""() => {
        const b = document.body.cloneNode(true);
        b.querySelectorAll('script, style, noscript, path, img[src^="data:"]').forEach(e => e.remove());
        return b.outerHTML;
    }""")
    (d / f"{name}.html").write_text(html, encoding="utf-8")
    print(f"Gespeichert: out/debug/{name}.png und {name}.html")


def install_hooks(f, manual_ai, draft, inspect=False):
    """Klinkt sich direkt vor dem Absenden in haziq ein: KI-Haken setzen, dann posten/planen oder Entwurf."""
    submit = f._submit_upload

    def hooked(page, *args, **kwargs):
        if inspect:
            input(">>> Oeffne im Browser die Sound-Bearbeitung (Fade-in/Lautstaerke sichtbar), dann hier Enter ... ")
            dump(page, "sound")
            input(">>> Oeffne jetzt die Cover-Bearbeitung ('Edit cover'), dann hier Enter ... ")
            dump(page, "cover")
            print("Fertig, nichts wurde gepostet. Schick mir die Dateien aus out/debug/")
            return "Error"
        ok = False if manual_ai else set_ai_label(page)
        if not ok:
            if not manual_ai:
                print("KI-Schalter nicht sicher erkannt.")
            input(">>> Setze im Browser 'AI-generated content' auf AN und druecke dann hier Enter ... ")
        if draft:
            page.click('button:has-text("Save draft")', timeout=10000)
            time.sleep(3)
            print("Als Entwurf gespeichert")
            return "Completed"
        return submit(page, *args, **kwargs)

    f._submit_upload = hooked


def upload(r, sound, headless, schedule):
    from tiktokautouploader import upload_tiktok
    vid = r["datei"][:-4]
    video = ROOT / "out" / "cut" / r["datei"]
    if not video.exists():
        sys.exit(f"{video} fehlt, erst rendern")
    text, tags = split_caption(r["caption"])
    kw = dict(hashtags=tags, headless=headless, stealth=True)
    if sound:
        kw.update(sound_name=sound, search_mode="favorites")
    if schedule:
        when = dt.datetime.fromisoformat(f"{r['datum']}T{r['uhrzeit']}")
        now = dt.datetime.now()
        if not dt.timedelta(minutes=20) < when - now < dt.timedelta(days=10):
            sys.exit(f"{vid}: {when} liegt nicht zwischen 20 Minuten und 10 Tagen in der Zukunft")
        if when.month != now.month:
            sys.exit(f"{vid}: {when:%d.%m.} ist im naechsten Monat, das kann der Kalender des Tools nicht, ab dem 1. einplanen")
        kw.update(schedule=r["uhrzeit"], day=when.day)
    print(f"--- {vid}: {r['datum']} {r['uhrzeit']} | {text[:50]}")
    upload_tiktok(str(video), text, ACCOUNT, **kw)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = sys.argv[1:]
    sound = opts[opts.index("--sound") + 1] if "--sound" in opts else SOUND
    if "--sound" in opts:
        args.remove(sound)
    at = opts[opts.index("--at") + 1] if "--at" in opts else None
    if at:
        args.remove(at)
    if "--account" in opts:
        ACCOUNT = opts[opts.index("--account") + 1]
        args.remove(ACCOUNT)
    cmd = args[0]
    if cmd == "shift":
        shift(args[1], args[2])
        sys.exit()

    import tiktokautouploader.function as f
    draft = cmd in ("test", "inspect") or "--draft" in opts
    install_hooks(f, "--manual-ai" in opts, draft, inspect=cmd == "inspect")
    first, last = args[1], args[2] if len(args) > 2 else args[1]
    for r in rows():
        if num(first) <= num(r["datei"][:-4]) <= num(last):
            if at:
                r["datum"], r["uhrzeit"] = at.split()
            upload(r, sound, "--headless" in opts, schedule=not draft)
            time.sleep(20)
