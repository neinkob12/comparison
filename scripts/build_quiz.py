"""Vertont ein Allgemeinwissen-Quiz (ElevenLabs mit Zeitstempeln) und schreibt die Timeline fuer Remotion.

Aufruf: python3 scripts/build_quiz.py q01 [q02 ...]
Liest content/quiz/<id>.json, schreibt video/public/audio/<id>/*.mp3 und video/public/timelines/<id>.json.
Hintergruende vorher laden: python3 scripts/fetch_backgrounds.py
"""
import base64, json, os, random, subprocess, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from build import FPS, PUB, ROOT, VOICE, frames, spoken, speed_for  # noqa: E402

TEMPO = 1.05
TIMER = 90       # Frames Bedenkzeit nach der Frage (3 s)
HOLD = 30        # Frames, in denen die Antwort nach dem Sprechen noch steht
TAIL = 30        # Frames Luft am Ende von Intro/Outro


def tts(text, out, tts_text=None):
    """Schreibt out (mp3) und out.json (Wort-Zeiten in Frames, bezogen auf die fertige Datei)."""
    meta = out.with_suffix(".json")
    if out.exists() and meta.exists():
        return json.loads(meta.read_text(encoding="utf-8"))
    say = spoken(tts_text or text)
    body = {"text": say, "model_id": "eleven_multilingual_v2", "language_code": "de",
            "voice_settings": {"stability": 0.7, "similarity_boost": 0.8, "style": 0, "speed": speed_for(say)}}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    for i in range(4):
        try:
            res = json.loads(urllib.request.urlopen(req, timeout=90).read())
            break
        except Exception:
            if i == 3:
                raise
            time.sleep(2 ** (i + 1))
    al = res["alignment"]
    chars, starts, ends = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    # Gesprochene Woerter mit Start/Ende aus den Zeichen-Zeiten
    spoken_words, cur = [], None
    for c, s, e in zip(chars, starts, ends):
        if c.isspace():
            cur = None
            continue
        if cur is None:
            cur = [c, s, e]
            spoken_words.append(cur)
        else:
            cur[0] += c
            cur[2] = e
    lead = max(0.0, spoken_words[0][1] - 0.03) if spoken_words else 0.0
    raw = out.with_suffix(".raw.mp3")
    raw.write_bytes(base64.b64decode(res["audio_base64"]))
    # Nur vorne Stille weg (Zeiten bleiben gueltig), dann etwas schneller
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{lead:.3f}", "-i", str(raw), "-af",
                    f"atempo={TEMPO},silenceremove=stop_periods=-1:stop_threshold=-45dB:stop_duration=0.6",
                    "-b:a", "128k", str(out)], check=True)
    raw.unlink()
    to_f = lambda t: round((t - lead) / TEMPO * FPS)  # noqa: E731
    timed = [(to_f(s), to_f(e)) for _, s, e in spoken_words]
    shown = text.split()
    if len(shown) == len(timed):
        words = [{"w": w, "s": s, "e": e} for w, (s, e) in zip(shown, timed)]
    else:
        # Untertitel weicht von der Aussprache ab (z.B. "Au" vs "A U"): Zeit nach Textlaenge verteilen
        t0, t1 = timed[0][0], timed[-1][1]
        total = sum(len(w) for w in shown)
        words, pos = [], 0
        for w in shown:
            s = t0 + (t1 - t0) * pos / total
            pos += len(w)
            words.append({"w": w, "s": round(s), "e": round(t0 + (t1 - t0) * pos / total)})
    meta.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    return words


def build(vid):
    v = json.loads((ROOT / "content" / "quiz" / f"{vid}.json").read_text(encoding="utf-8"))
    adir = PUB / "audio" / vid
    adir.mkdir(parents=True, exist_ok=True)
    segs = []

    def voice(name, text, tts_text=None):
        f = adir / f"{name}.mp3"
        words = tts(text, f, tts_text)
        return f"audio/{vid}/{f.name}", frames(f), words

    # Jede Frage eigener Naturclip, Reihenfolge pro Video gemischt; Musik rotiert, falls nicht gesetzt
    rnd = random.Random(vid)
    clips = sorted(p.stem for p in (PUB / "bg").glob("*.mp4"))
    rnd.shuffle(clips)
    bgs = (v.get("bg") or []) + [c for c in clips if c not in (v.get("bg") or [])]
    bg = lambda k: {"bg": f"bg/{bgs[k % len(bgs)]}.mp4", "bgFrom": rnd.randint(0, 300)}  # noqa: E731
    tracks = sorted(p.name for p in (PUB / "music").glob("*.mp3"))
    music = v.get("music") or (tracks[sum(map(ord, vid)) % len(tracks)].removesuffix(".mp3") if tracks else None)

    i = v["intro"]
    # Jedes Video startet mit "Allgemeinwissen Quiz", danach die eigene Hook
    audio, sp, words = voice("00_intro", "Allgemeinwissen Quiz! " + i["say"], i.get("tts") and "Allgemeinwissen Quiz! " + i["tts"])
    segs.append({"kind": "intro", "audio": audio, "words": words, "speak": sp, "title": i["title"], "sub": i.get("sub", ""),
                 "duration": sp + TAIL, **bg(0)})
    for n, q in enumerate(v["questions"], 1):
        qa, qsp, qw = voice(f"{n:02d}_q", q["say"], q.get("tts"))
        aa, asp, aw = voice(f"{n:02d}_a", q["answer"], q.get("answerTts"))
        revealAt = qsp + TIMER
        segs.append({"kind": "q", "n": n, "say": q["say"], "answer": q["answer"], **bg(n),
                     "audio": qa, "words": qw, "speak": qsp, "timer": TIMER,
                     "answerAudio": aa, "answerWords": aw, "revealAt": revealAt,
                     "duration": revealAt + asp + HOLD})
    o = v["outro"]
    audio, sp, words = voice(f"{len(v['questions']) + 1:02d}_outro", o["say"], o.get("tts"))
    segs.append({"kind": "outro", "audio": audio, "words": words, "speak": sp, "title": o["title"], "sub": o.get("sub", ""),
                 "duration": sp + TAIL + 30, **bg(len(v["questions"]) + 1)})

    total = sum(s["duration"] for s in segs)
    tl = {"id": vid, "format": "quiz", "channel": v["channel"], "handle": v.get("handle"), "fps": FPS,
          "durationInFrames": total, "music": f"music/{music}.mp3" if music else None,
          "items": [{"answer": q["answer"]} for q in v["questions"]], "segments": segs}
    (PUB / "timelines").mkdir(parents=True, exist_ok=True)
    (PUB / "timelines" / f"{vid}.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{vid}: {total / FPS:.1f} s, {len(segs)} Abschnitte")


if __name__ == "__main__":
    for vid in sys.argv[1:]:
        build(vid)
