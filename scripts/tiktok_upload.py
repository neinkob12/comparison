"""TikTok-Upload kostenlos ueber den Browser (haziq-exe/TikTokAutoUploader), fuer mehrere Konten.

Laeuft auf deinem eigenen Rechner (Heim-Internet), NICHT in der Cloud. Einrichtung: docs/SETUP.md

Konten stehen in config/accounts.json (Plan-Datei, Sound, Lautstaerke, Fade-in, Cover-Sekunde).
Jeder erfolgreiche Upload landet in docs/upload_log.csv und wird automatisch nach GitHub gepusht,
damit alle sehen, was schon eingeplant ist. Schon eingeplante Videos werden uebersprungen.

Benutzung (aus dem Repo-Ordner, KONTO = Name aus config/accounts.json):
  python scripts/tiktok_upload.py status                       # Ueberblick aller Konten
  python scripts/tiktok_upload.py test a17 --account KONTO     # 1 Video als Entwurf
  python scripts/tiktok_upload.py plan a17 a50 --account KONTO # einplanen laut Plan (max. 10 Tage voraus)
  python scripts/tiktok_upload.py mark a01 a16 --account KONTO # von Hand gepostete Videos als erledigt eintragen
  python scripts/tiktok_upload.py shift a17 2026-10-19 --account KONTO   # Plan ab a17 neu datieren, 4 pro Tag
  python scripts/tiktok_upload.py inspect a17 --account KONTO  # postet nichts, speichert Sound-/Cover-Ansicht nach out/debug/

Optionen:
  --at "JJJJ-MM-TT HH:MM"  andere Uhrzeit als im Plan (Minuten in 5er-Schritten), z.B. fuer Tests
  --draft          nur als Entwurf speichern
  --force          auch Videos hochladen, die laut Log schon eingeplant sind
  --manual-ai      vor jedem Absenden anhalten, du setzt den KI-Haken selbst und drueckst Enter
  --headless       Browser unsichtbar (erst nutzen, wenn die Tests sauber laufen)

Beim ersten Start pro Konto oeffnet sich ein Login-Fenster (siehe docs/SETUP.md). Die Sitzung liegt dann in
TK_cookies_<konto>.json (wie ein Passwort behandeln, ist in .gitignore, nie teilen).
"""
import csv, datetime as dt, json, random, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows-Konsole: Emojis/Umlaute in Ausgaben
ROOT = Path(__file__).resolve().parent.parent
ACCOUNTS = ROOT / "config" / "accounts.json"
LOG = ROOT / "docs" / "upload_log.csv"
DONE = ("geplant", "manuell")  # Modi, die als erledigt zaehlen
LOG_FIELDS = ["zeit", "konto", "video", "geplant_fuer", "modus", "von"]
TIMES = ["12:30", "16:00", "18:30", "21:00"]
PAUSE_S = (120, 240)  # Sekunden Pause zwischen zwei Uploads (zufaellig), schuetzt vor IP-Sperren
# Standardwerte, pro Konto in config/accounts.json ueberschreibbar
ACCOUNT, PLAN, SOUND = None, None, ""
MUSIC_DB = "-12"     # Lautstaerke des TikTok-Sounds
FADE_IN = "2.5"      # Sekunden
COVER_AT = "5"       # Sekunde, aus der das Cover geschnitten wird, falls kein out/cover/<id>.jpg existiert
CURRENT = {}
AI_TEXT = re.compile(r"AI[- ]generated content|KI-generierte", re.I)


def accounts():
    return json.loads(ACCOUNTS.read_text(encoding="utf-8"))


def rows(plan=None):
    p = ROOT / (plan or PLAN)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if p.exists() else []


def num(vid):
    return int(re.sub(r"\D", "", vid))


def shift(start_vid, start_date):
    rs, day, slot = rows(), dt.date.fromisoformat(start_date), 0
    for r in rs:
        if num(r["datei"][:-4]) >= num(start_vid):
            r["datum"], r["uhrzeit"] = day.isoformat(), TIMES[slot]
            slot = (slot + 1) % len(TIMES)
            day += dt.timedelta(days=slot == 0)
    with open(ROOT / PLAN, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rs[0].keys(), lineterminator="\n")
        w.writeheader()
        w.writerows(rs)
    print(f"Plan ab {start_vid} startet jetzt am {start_date}, letztes Video: {rs[-1]['datum']} {rs[-1]['uhrzeit']}")


def log_rows():
    return list(csv.DictReader(open(LOG, encoding="utf-8"))) if LOG.exists() else []


def already_scheduled(vid):
    return any(l["konto"] == ACCOUNT and l["video"] == vid and l["modus"] in DONE for l in log_rows())


def write_log(vid, when, mode):
    new = not LOG.exists()
    who = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS, lineterminator="\n")
        if new:
            w.writeheader()
        w.writerow({"zeit": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "konto": ACCOUNT, "video": vid,
                    "geplant_fuer": when, "modus": mode, "von": who or "?"})


def push_log(summary):
    """Log nach GitHub, damit alle den Stand sehen. Scheitert das, bleibt es lokal und wird beim naechsten Mal mitgenommen."""
    def git(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    git("add", str(LOG.relative_to(ROOT)))
    if git("diff", "--cached", "--quiet").returncode == 0:
        return
    git("commit", "-m", f"Upload-Log: {summary}", "--", str(LOG.relative_to(ROOT)))
    pull = git("pull", "--rebase", "--autostash")
    push = git("push")
    if pull.returncode or push.returncode:
        err = (pull.stderr if pull.returncode else push.stderr).strip().splitlines()
        print("Log nur lokal gespeichert (git pull/push ging nicht): " + (err[-1] if err else "?"))
        print("Spaeter: git pull --rebase && git push")
    else:
        print("Log nach GitHub gepusht.")


def status():
    log = log_rows()
    now = dt.datetime.now()
    for name, cfg in accounts().items():
        mine = [l for l in log if l["konto"] == name and l["modus"] in DONE]
        done = {l["video"] for l in mine}
        future = sorted(l["geplant_fuer"] for l in mine if l["geplant_fuer"] >= now.strftime("%Y-%m-%d %H:%M"))
        plan = rows(cfg.get("plan"))
        todo = [r["datei"][:-4] for r in plan if r["datei"][:-4] not in done]
        print(f"\n{name}  (betreut von {cfg.get('betreut_von', '?')})")
        if not plan:
            print(f"  kein Plan ({cfg.get('plan')})")
            continue
        if future:
            days = (dt.datetime.fromisoformat(future[-1]) - now).days
            print(f"  eingeplant: {len(future)} Videos, letztes {future[-1]} (noch ~{days} Tage abgedeckt)")
        else:
            print("  nichts eingeplant!")
        print(f"  noch offen im Plan: {len(todo)}" + (f", naechstes: {todo[0]}" if todo else ""))


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


def fill_after(page, label, value):
    """Tippt value in das erste Textfeld (kein Slider) nach der Beschriftung label, prueft danach den Wert."""
    lab = page.get_by_text(label, exact=True).first
    if not lab.count() or not lab.is_visible():
        return False
    inp = lab.locator('xpath=following::input[not(@type="range")][1]')
    inp.click()
    inp.fill(value)
    inp.press("Enter")
    time.sleep(0.5)
    try:
        return float(inp.input_value().replace(",", ".")) == float(value)
    except ValueError:
        return False


def set_audio(page, sound):
    """Im Sound-Editor: Lautstaerke und Fade-in des eingefuegten Sounds setzen."""
    time.sleep(2)
    if not page.get_by_text("Fade-in duration", exact=True).first.is_visible():
        clip = page.get_by_text(re.compile(re.escape(sound), re.I)).last
        if clip.count():
            clip.click()
            time.sleep(1)
    ok = fill_after(page, "Volume", MUSIC_DB) and fill_after(page, "Fade-in duration", FADE_IN)
    if ok:
        print(f"Sound: {MUSIC_DB} dB, Fade-in {FADE_IN} s")
    else:
        input(f">>> Setze im Browser Volume auf {MUSIC_DB} dB und Fade-in auf {FADE_IN} s, dann hier Enter ... ")


def make_cover(vid, video):
    for ext in ("jpg", "png"):
        c = ROOT / "out" / "cover" / f"{vid}.{ext}"
        if c.exists():
            return c
    c.parent.mkdir(parents=True, exist_ok=True)
    c = c.with_suffix(".jpg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", COVER_AT, "-i", str(video),
                    "-frames:v", "1", "-q:v", "2", str(c)], check=True)
    return c


def set_cover(page, img):
    try:
        page.get_by_text("Edit cover", exact=True).first.click()
        page.get_by_text("Upload cover", exact=True).first.wait_for(timeout=15000)
        time.sleep(1)
        with page.expect_file_chooser() as fc:
            page.get_by_text("Upload cover", exact=True).first.click()
        fc.value.set_files(str(img))
        time.sleep(4)
        # Save oben rechts im Cover-Editor: nur sichtbare Buttons mit genau "Save" (nicht "Save draft")
        modal = page.get_by_text("Preview in profile", exact=False).first
        saves = page.locator("button:visible").filter(has_text=re.compile(r"^\s*Save\s*$"))
        for i in reversed(range(saves.count())):
            saves.nth(i).click()
            time.sleep(2)
            if not modal.is_visible():
                break
        if modal.is_visible():
            raise RuntimeError("Cover-Editor noch offen")
        print(f"Cover hochgeladen: {img.name}")
    except Exception as e:
        print(f"Cover automatisch nicht moeglich ({type(e).__name__}).")
        input(f">>> Lade im Browser das Cover {img} hoch und speichere, dann hier Enter ... ")


def type_tag(page, tag):
    """Hashtag tippen; Umlaute direkt einfuegen, weil Tastatur-Tippen sie verschluckt (#würdestdueher)."""
    for ch in tag:
        if ch.isascii():
            page.keyboard.type(ch)
        else:
            page.keyboard.insert_text(ch)
    time.sleep(0.8)
    try:
        page.click(f'span.hash-tag-topic:has-text("{tag}")', timeout=1500)
    except Exception:
        page.keyboard.type(" ")


def dismiss_tour(page):
    """TikTok-Einfuehrungstour (react-joyride) wegklicken, ihr Overlay blockiert sonst alle Klicks."""
    time.sleep(1)
    for sel in ('[data-test-id="button-skip"]', '[data-test-id="button-close"]', '[data-test-id="button-primary"]'):
        for _ in range(6):
            b = page.locator(sel)
            if not (b.count() and b.first.is_visible()):
                break
            b.first.click(force=True)
            time.sleep(0.5)
    page.keyboard.press("Escape")
    page.evaluate("document.querySelectorAll('#react-joyride-portal, .react-joyride__overlay, .react-joyride__spotlight')"
                  ".forEach(e => e.remove())")


def install_hooks(f, manual_ai, draft, inspect=False):
    """Klinkt sich in haziq ein: Hashtags mit Umlauten, Sound-Einstellungen, Cover, KI-Haken, dann posten/planen oder Entwurf."""
    submit = f._submit_upload
    describe = f._add_description_and_hashtags

    def described(page, sim, video, description, hashtags, stealth, suppressprint):
        page.wait_for_selector('div[data-contents="true"]')
        dismiss_tour(page)
        describe(page, sim, video, description, None, stealth, suppressprint)
        for tag in hashtags or []:
            type_tag(page, tag if tag.startswith("#") else "#" + tag)

    f._add_description_and_hashtags = described
    pick = f._pick_sound

    def picked(page, sound_name, *args, **kwargs):
        pick(page, sound_name, *args, **kwargs)
        set_audio(page, sound_name)

    f._pick_sound = picked

    def hooked(page, *args, **kwargs):
        if inspect:
            input(">>> Oeffne im Browser die Sound-Bearbeitung (Fade-in/Lautstaerke sichtbar), dann hier Enter ... ")
            dump(page, "sound")
            input(">>> Oeffne jetzt die Cover-Bearbeitung ('Edit cover'), dann hier Enter ... ")
            dump(page, "cover")
            print("Fertig, nichts wurde gepostet. Schick mir die Dateien aus out/debug/")
            return "Error"
        if CURRENT.get("cover"):
            set_cover(page, CURRENT["cover"])
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
    CURRENT["cover"] = make_cover(vid, video)
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
    print(f"--- {ACCOUNT} {vid}: {r['datum']} {r['uhrzeit']} | {text[:50]}")
    return upload_tiktok(str(video), text, ACCOUNT, **kw)


if __name__ == "__main__":
    opts = sys.argv[1:]
    args, i = [], 0
    while i < len(opts):
        if opts[i] in ("--at", "--account", "--sound"):
            i += 2
            continue
        if not opts[i].startswith("--"):
            args.append(opts[i])
        i += 1
    val = lambda o: opts[opts.index(o) + 1] if o in opts else None
    cmd = args[0] if args else "status"
    if cmd == "status":
        status()
        sys.exit()

    accs = accounts()
    ACCOUNT = val("--account") or (next(iter(accs)) if len(accs) == 1 else None)
    if ACCOUNT not in accs:
        sys.exit(f"Bitte --account angeben, eins von: {', '.join(accs)} (neue Konten in config/accounts.json eintragen)")
    cfg = accs[ACCOUNT]
    PLAN = cfg["plan"]
    SOUND = val("--sound") or cfg.get("sound", "")
    MUSIC_DB, FADE_IN, COVER_AT = (str(cfg.get(k, d)) for k, d in
                                   (("music_db", MUSIC_DB), ("fade_in", FADE_IN), ("cover_at", COVER_AT)))
    if cmd == "shift":
        shift(args[1], args[2])
        sys.exit()
    if cmd == "mark":  # von Hand gepostete Videos als erledigt eintragen
        marked = [r["datei"][:-4] for r in rows() if num(args[1]) <= num(r["datei"][:-4]) <= num(args[-1])]
        for r in rows():
            if r["datei"][:-4] in marked:
                write_log(r["datei"][:-4], f"{r['datum']} {r['uhrzeit']}", "manuell")
        push_log(f"{ACCOUNT} {marked[0]}-{marked[-1]} manuell")
        sys.exit()

    import tiktokautouploader.function as f
    draft = cmd in ("test", "inspect") or "--draft" in opts
    install_hooks(f, "--manual-ai" in opts, draft, inspect=cmd == "inspect")
    first, last = args[1], args[2] if len(args) > 2 else args[1]
    at, done, failed, handled, streak = val("--at"), [], [], 0, 0
    for r in rows():
        vid = r["datei"][:-4]
        if not num(first) <= num(vid) <= num(last):
            continue
        if at:
            r["datum"], r["uhrzeit"] = at.split()
        if not draft and already_scheduled(vid) and "--force" not in opts:
            print(f"{vid} ist laut Log schon eingeplant, uebersprungen (--force zum Erzwingen)")
            continue
        if handled:  # ruhig bleiben: zufaellige Pause zwischen den Videos, wie ein Mensch
            pause = random.randint(*PAUSE_S)
            print(f"Pause {pause} s ...")
            time.sleep(pause)
        handled += 1
        try:
            ok = upload(r, SOUND, "--headless" in opts, schedule=not draft) == "Completed"
        except Exception as e:
            print(f"FEHLER bei {vid}: {str(e).splitlines()[0][:200]}")
            ok = False
        if ok and cmd != "inspect":
            write_log(vid, f"{r['datum']} {r['uhrzeit']}", "entwurf" if draft else "geplant")
            done.append(vid)
        elif not ok and cmd != "inspect":
            failed.append(vid)
        streak = 0 if ok else streak + 1
        if streak >= 2:
            print("2 Fehler hintereinander: Abbruch, damit TikTok uns nicht sperrt. Spaeter erneut versuchen.")
            break
    print(f"\nFertig: {len(done)} ok" + (f", fehlgeschlagen: {', '.join(failed)}" if failed else ""))
    if done:
        push_log(f"{ACCOUNT} {done[0]}-{done[-1]}")
