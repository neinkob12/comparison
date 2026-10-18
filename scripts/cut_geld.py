"""Kuerzt die Geld-Videos auf max. 65 s, indem ganze Abschnitte rausgeschnitten werden (ohne Neu-Rendern).

Wo nach dem Schnitt der Claim nicht mehr stimmt ("alle drei" -> "beide"), wird nur das Intro
(ca. 3 s) mit neuem Text neu gerendert und vorne eingesetzt.
Aufruf: python3 scripts/cut_geld.py g01 g02 ...   -> out/cut/gNN.mp4, Schnittliste in content/cuts.json
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402

MAX_S = 65.0
# Segment-Indizes der Timeline, die rausfliegen (0 = Intro, letzter = Outro).
# Erste Frage bleibt immer drin, weil dort die Follow-Einblendung liegt.
PLAN = {
    "g01": {"drop": [6, 7], "claim": {"title": "NUR 15%", "sub": "ANTWORTEN RICHTIG", "say": "Nur 15 Prozent beantworten beide richtig!"}},
    "g02": {"drop": [3, 4]},
    "g03": {"drop": [6, 7], "claim": {"title": "NUR 1 VON 10", "sub": "SCHAFFT BEIDE", "say": "Nur einer von zehn schafft beide!"}},
    "g04": {"drop": [8]},
    "g05": {"drop": [6]},
    "g06": {"drop": [2, 4]},
}


def new_intro(vid, claim):
    """Rendert nur das Intro mit neuem Claim, gibt Pfad zum MP4 zurueck."""
    v = json.loads((ROOT / "content" / "videos" / f"{vid}.json").read_text())
    tl = json.loads((build.PUB / "timelines" / f"{vid}.json").read_text())
    f = build.PUB / "audio" / vid / "claim_cut.mp3"
    build.tts(claim["say"], f, v.get("voice"))
    sp = build.frames(f)
    intro = {**tl["segments"][0], "audio": f"audio/{vid}/{f.name}", "speak": sp,
             "title": claim["title"], "sub": claim["sub"], "hold": 18}
    intro["duration"] = sp + intro["hold"]
    iid = f"{vid}_intro"
    (build.PUB / "timelines" / f"{iid}.json").write_text(json.dumps(
        {**tl, "id": iid, "durationInFrames": intro["duration"], "segments": [intro]}, ensure_ascii=False, indent=1))
    subprocess.run(["node", "scripts/render.mjs", iid], cwd=ROOT / "video", check=True, capture_output=True)
    return ROOT / "out" / f"{iid}.mp4", intro["duration"]


def cut(vid):
    p = PLAN[vid]
    tl = json.loads((build.PUB / "timelines" / f"{vid}.json").read_text())
    segs, fps = tl["segments"], tl["fps"]
    inputs = ["-i", str(ROOT / "out" / f"{vid}.mp4")]
    keep, start = [], 0
    for i, s in enumerate(segs):
        if i not in p["drop"]:
            keep.append([0, start, start + s["duration"]])
        start += s["duration"]
    if p.get("claim"):
        f, dur = new_intro(vid, p["claim"])
        inputs += ["-i", str(f)]
        keep[0] = [1, 0, dur]
    # Noch zu lang? Stille am Outro-Ende kuerzen (max. 40 Frames)
    total = sum(e - s for _, s, e in keep)
    excess = max(0, total - int(MAX_S * fps))
    trim = min(excess, 40)
    keep[-1][2] -= trim
    total -= trim
    excess -= trim
    # Dann gleichmaessig Standzeit am Ende der Fragen/Aufloesungen (max. 10 Frames je Abschnitt)
    mids = keep[1:-1]
    for _ in range(10):
        for k in mids:
            if excess > 0:
                k[2] -= 1; total -= 1; excess -= 1
    if total > MAX_S * fps:
        raise SystemExit(f"{vid}: immer noch {total / fps:.1f} s")
    parts, labels = [], []
    for j, (src, s0, s1) in enumerate(keep):
        parts.append(f"[{src}:v]trim=start_frame={s0}:end_frame={s1},setpts=PTS-STARTPTS[v{j}];"
                     f"[{src}:a]atrim=start={s0 / fps}:end={s1 / fps},asetpts=PTS-STARTPTS[a{j}];")
        labels.append(f"[v{j}][a{j}]")
    fc = "".join(parts) + "".join(labels) + f"concat=n={len(keep)}:v=1:a=1[v][a]"
    out = ROOT / "out" / "cut" / f"{vid}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-c:a", "aac",
                    "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    return {"removed_segments": p["drop"], "new_claim": bool(p.get("claim")), "seconds": round(total / fps, 1)}


if __name__ == "__main__":
    path = ROOT / "content" / "cuts.json"
    cuts = json.loads(path.read_text()) if path.exists() else {}
    for vid in sys.argv[1:]:
        cuts[vid] = cut(vid)
        print(vid, cuts[vid])
    path.write_text(json.dumps(dict(sorted(cuts.items())), indent=1))
