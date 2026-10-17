"""Vertont ein Video (ElevenLabs) und schreibt die Timeline fuer Remotion.

Aufruf: python3 scripts/build.py a01 [b01 ...]
Liest content/videos/<id>.json, schreibt video/public/audio/<id>/*.mp3 und video/public/timelines/<id>.json.
"""
import json, os, re, shutil, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "video" / "public"
FPS = 30
VOICE = "pNInz6obpgDQGcFmaJgB"  # Adam
GAP = 81          # Frames 3-2-1-Timer nach der Frage (2.7 s)
HOOK_GAP = 45     # Hook-Timer zeigt 3 s, laeuft aber in 1.5 s ab
TEMPO = 1.05      # Stimme etwas schneller als ElevenLabs max. 1.2
HOOK_TEMPO = 1.12 # Hook noch schneller
REVEAL = 45       # Frames, in denen die Prozente stehen
TAIL = 15         # Frames Luft am Ende von Intro/Outro

pron = json.loads((ROOT / "config" / "aussprache.json").read_text())
speeds = pron.pop("_speed", {})
pron = {k: v for k, v in pron.items() if not k.startswith("_")}
keys = sorted(pron, key=len, reverse=True)


def spoken(text):
    # [[...]] bleibt roh (Slop-Aussprache), alles andere bekommt die Lautschrift
    parts = re.split(r"(\[\[.*?\]\])", text)
    out = []
    for p in parts:
        if p.startswith("[["):
            out.append(p[2:-2]); continue
        for k in keys:
            p = re.sub(r"(?<![\w])" + re.escape(k) + r"(?![\w])", pron[k], p)
        out.append(p)
    return "".join(out)


def speed_for(text):
    return min(1.2, max([speeds[n] for n in speeds if n in text] + [1.18]))


def tts(text, out, voice=None, tempo=TEMPO):
    if out.exists():
        return
    # Optional pro Video: {"id": ..., "speed": ..., "stability": ...}, sonst Adam wie bisher
    voice = voice or {}
    body = {"text": spoken(text), "model_id": "eleven_multilingual_v2", "language_code": "de",
            "voice_settings": {"stability": voice.get("stability", 0.7), "similarity_boost": 0.8, "style": voice.get("style", 0),
                               "speed": voice.get("speed") or speed_for(text)}}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice.get('id', VOICE)}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    raw = out.with_suffix(".raw.mp3")
    for i in range(4):
        try:
            raw.write_bytes(urllib.request.urlopen(req, timeout=90).read())
            break
        except Exception:
            if i == 3:
                raise
            __import__("time").sleep(2 ** (i + 1))
    # Stille vorne/hinten weg, Atempausen im Satz auf max. 0.25 s kuerzen
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_threshold=-45dB:stop_duration=0.25,"
                    f"atempo={tempo}",
                    "-b:a", "128k", str(out)], check=True)
    raw.unlink()


def frames(path):
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                       "-of", "csv=p=0", str(path)]).decode())
    return int(d * FPS) + 1


def copy_img(rel):
    if not rel:
        return None
    src = ROOT / "assets" / rel
    if not src.exists():
        print("  fehlt:", rel)
        return None
    dst = PUB / "img" / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return "img/" + rel


def build(vid):
    v = json.loads((ROOT / "content" / "videos" / f"{vid}.json").read_text())
    adir = PUB / "audio" / vid
    adir.mkdir(parents=True, exist_ok=True)
    segs = []
    voice = v.get("voice")
    say_ = lambda text, out, tempo=TEMPO: tts(text, out, voice, tempo)  # noqa: E731

    def add(kind, n, data, say, extra):
        f = adir / f"{n:02d}_{kind}.mp3"
        say_(say, f)
        segs.append({"kind": kind, "audio": f"audio/{vid}/{f.name}", "speak": frames(f), **extra, **data})

    n = 0
    if v.get("intro"):
        # Fertige epische Ansage (eleven_v3, mit Hall), Intro max. 2 s
        i = v["intro"]
        f = PUB / "sfx" / "intro_rapper_duell.mp3"
        sp = frames(f)
        segs.append({"kind": "intro", "audio": "sfx/intro_rapper_duell.mp3", "speak": sp, "voiceAt": 6,
                     "title": i["title"], "sub": i["sub"], "hold": max(54, sp + 10) - sp}); n += 1
    if v.get("claim"):
        # Einblendung + Ansage am Anfang, z.B. "80% antworten falsch"
        c = v["claim"]
        f = adir / f"{n:02d}_claim.mp3"
        say_(c["say"], f)
        sp = frames(f)
        segs.append({"kind": "intro", "audio": f"audio/{vid}/{f.name}", "speak": sp, "voiceAt": 6,
                     "title": c["title"], "sub": c["sub"], "hold": 6 + 12}); n += 1
    qs = ([v["hook"]] if v.get("hook") else []) + v["questions"]
    num = 0
    for q in qs:
        kind = q.get("type", "q")
        if kind == "q":
            num += 1
        side = lambda s: {"label": s["label"], "img": copy_img(s.get("img")), "emoji": s.get("emoji")}
        # Frage in zwei Teile: erst Option A, dann ab "oder" Option B (fliegt dann rein)
        say = q["say"]
        m = re.search(r",?\s+oder\s+", say)
        fa = adir / f"{n:02d}_{kind}_a.mp3"
        fb = adir / f"{n:02d}_{kind}_b.mp3"
        tempo = HOOK_TEMPO if kind == "hook" else TEMPO
        gap = HOOK_GAP if kind == "hook" else GAP
        if m:
            say_(say[:m.start()] + ",", fa, tempo); say_("oder " + say[m.end():], fb, tempo)
            ba = frames(fa) + 2
            sp = ba + frames(fb)
            seg = {"kind": kind, "audio": f"audio/{vid}/{fa.name}", "audioB": f"audio/{vid}/{fb.name}",
                   "bAt": ba, "speak": sp, "gap": gap, "hold": REVEAL,
                   "a": side(q["a"]), "b": side(q["b"]), "pct": q["pct"]}
            if q.get("winSay"):
                fw = adir / f"{n:02d}_{kind}_win.mp3"
                say_(q["winSay"], fw)
                seg["winAudio"] = f"audio/{vid}/{fw.name}"
                seg["hold"] = max(REVEAL, 12 + frames(fw) + 8)
            if kind == "hook":
                seg["banner"] = q.get("banner", "WAS WÄHLT DIE MEHRHEIT? 👀")
            segs.append(seg)
            if q.get("explain"):
                # Aufloesung: erst Fakt A, dann Fakt B, dann Urteil
                e = q["explain"]
                parts = {}
                for key, text in (("a", e["a"]["say"]), ("b", e["b"]["say"]), ("win", e["winSay"])):
                    fe = adir / f"{n:02d}_explain_{key}.mp3"
                    say_(text, fe)
                    parts[key] = (f"audio/{vid}/{fe.name}", frames(fe))
                bAt = 8 + parts["a"][1] + 8
                winAt = bAt + parts["b"][1] + 8
                exp = {"kind": "explain", "audio": parts["a"][0], "audioB": parts["b"][0], "winAudio": parts["win"][0],
                       "aAt": 8, "bAt": bAt, "winAt": winAt, "speak": winAt + parts["win"][1], "hold": 30,
                       "best": e["best"], "note": e.get("note", "Vereinfacht gerechnet. Keine Anlageberatung."),
                       "a": {**side(q["a"]), "fact": e["a"]["fact"]}, "b": {**side(q["b"]), "fact": e["b"]["fact"]}}
                segs.append(exp)
        else:
            add(kind, n, {"a": side(q["a"]), "b": side(q["b"]), "pct": q["pct"]}, say, {"gap": gap, "hold": REVEAL})
        n += 1
    o = v["outro"]
    add("outro", n, {"title": o.get("title"), "sub": o.get("sub"), "share": o.get("share")},
        o["say"] + (" " + o["shareSay"] if o.get("shareSay") else ""), {"hold": TAIL + 30})

    for s in segs:
        s["duration"] = s["speak"] + s.get("gap", 0) + s["hold"]
    total = sum(s["duration"] for s in segs)
    tl = {"id": vid, "channel": v["channel"], "handle": v.get("handle"), "fps": FPS,
          "durationInFrames": total, "segments": segs}
    (PUB / "timelines").mkdir(parents=True, exist_ok=True)
    (PUB / "timelines" / f"{vid}.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))
    print(f"{vid}: {total / FPS:.1f} s, {len(segs)} Abschnitte")


if __name__ == "__main__":
    for vid in sys.argv[1:]:
        build(vid)
