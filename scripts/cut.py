"""Kuerzt fertige Videos auf 60-65 s, indem 2 Fragen rausgeschnitten werden (ohne Neu-Rendern).

Geschuetzt: Hook, 1. Frage (Follow-Einblendung), Zwischenfrage, Outro, Fragen mit Spitzname oder TTS-Effekt.
Bevorzugt raus: Paarungen, die ueber alle Videos am haeufigsten vorkommen.
Aufruf: python3 scripts/cut.py a01 a02 ...   -> out/cut/aNN.mp4, Schnittliste in content/cuts.json
"""
import itertools, json, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import generate as g  # noqa: E402

MIN_S, MAX_S, TARGET = 60.0, 65.0, 62.5
NICKS = {n for v in g.ARTISTS.values() for n in v[2]}


def pair_key(q):
    a, b = g.IMG.get(q["a"].get("img")), g.IMG.get(q["b"].get("img"))
    return (a[0],) + tuple(sorted((a[1], b[1]))) if a and b else None


def all_pair_counts():
    c = Counter()
    for f in (ROOT / "content" / "videos").glob("a*.json"):
        v = json.loads(f.read_text())
        for q in [v["hook"]] + v["questions"]:
            if q.get("type") != "mid" and pair_key(q):
                c[pair_key(q)] += 1
    return c


def protected(q):
    if q.get("type") == "mid" or "[[" in q["say"]:
        return True
    return any(n in q["a"]["label"] or n in q["b"]["label"] for n in NICKS)


def plan(vid, counts):
    v = json.loads((ROOT / "content" / "videos" / f"{vid}.json").read_text())
    tl = json.loads((ROOT / "video" / "public" / "timelines" / f"{vid}.json").read_text())
    segs = tl["segments"]
    fps = tl["fps"]
    # Segment 0 = Hook, 1..8 = Fragen (inkl. Zwischenfrage), 9 = Outro
    qs = v["questions"]
    total = sum(s["duration"] for s in segs) / fps
    cand = [i for i in range(1, len(qs)) if not protected(qs[i])]  # Frage 0 (Index 1) bleibt
    if len(cand) < 2:
        cand = [i for i in range(1, len(qs)) if qs[i].get("type") != "mid"]
    best = None
    for a, b in itertools.combinations(cand, 2):
        t = total - (segs[a + 1]["duration"] + segs[b + 1]["duration"]) / fps
        ok = MIN_S <= t <= MAX_S + 3  # bis 3 s drueber wird danach weggetrimmt
        score = (0 if ok else 1, abs(t - TARGET), -(counts[pair_key(qs[a])] + counts[pair_key(qs[b])]))
        if best is None or score < best[0]:
            best = (score, (a, b), t)
    return segs, fps, best[1], best[2]


def cut(vid, counts):
    segs, fps, (a, b), t = plan(vid, counts)
    t = float(t)
    drop = {a + 1, b + 1}
    # Zu lang? Erst stilles Outro-Ende kuerzen, dann Standzeit nach der Aufloesung (gleichmaessig)
    excess = max(0, round((t - (MAX_S - 0.5)) * fps))
    trim = {i: 0 for i in range(len(segs))}
    out_room = min(40, segs[-1]["hold"] - 10)
    trim[len(segs) - 1] = min(excess, out_room)
    excess -= trim[len(segs) - 1]
    room = {i: (6 if segs[i].get("winAudio") else 22) for i in range(1, len(segs) - 1) if i not in drop}
    while excess > 0 and any(room[i] > trim[i] for i in room):
        for i in room:
            if excess > 0 and trim[i] < room[i]:
                trim[i] += 1
                excess -= 1
    t -= sum(trim.values()) / fps
    start = 0
    keep = []
    for i, s in enumerate(segs):
        if i not in drop:
            keep.append((start, start + s["duration"] - trim[i]))
        start += s["duration"]
    parts, labels = [], []
    for j, (s0, s1) in enumerate(keep):
        parts.append(f"[0:v]trim=start_frame={s0}:end_frame={s1},setpts=PTS-STARTPTS[v{j}];"
                     f"[0:a]atrim=start={s0 / fps}:end={s1 / fps},asetpts=PTS-STARTPTS[a{j}];")
        labels.append(f"[v{j}][a{j}]")
    fc = "".join(parts) + "".join(labels) + f"concat=n={len(keep)}:v=1:a=1[v][a]"
    out = ROOT / "out" / "cut" / f"{vid}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(ROOT / "out" / f"{vid}.mp4"), "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-c:a", "aac",
                    "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    return {"removed_questions": [a, b], "seconds": round(t, 1)}


if __name__ == "__main__":
    counts = all_pair_counts()
    path = ROOT / "content" / "cuts.json"
    cuts = json.loads(path.read_text()) if path.exists() else {}
    for vid in sys.argv[1:]:
        cuts[vid] = cut(vid, counts)
        print(vid, cuts[vid])
    path.write_text(json.dumps(dict(sorted(cuts.items())), indent=1))
