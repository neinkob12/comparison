"""Schreibt die Video-Skripte fuer Kanal A (content/videos/aNN.json).

Regeln (von Jakob):
- pro Video genau 1 Spitzname/Fake-Name
- pro Video mindestens 2 weirde TTS-Effekte (in [[...]], werden nicht umgeschrieben)
- Haribo gewinnt -> manchmal "Ohne Finger, Akh!" nach der Aufloesung
- Prozente teils extrem (1/99), teils knapp
Aufruf: python3 scripts/generate.py 2 50
"""
import json, random, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "videos"

# key: (Anzeigename, Bild, Spitznamen, Slop-Varianten)
ARTISTS = {
    "nizi": ("Nizi19", "artists/nizi19.jpg", ["Nils Zimmermann", "Doktor19"], ["Nisssssiiiiiijaaaaaaa", "Niiiiiiiisssssiiiii"]),
    "lucio": ("Lucio", "artists/lucio101.jpg", ["Luciano"], ["Luuuuuussssiiiiiooooo", "Lussssssiiiiiiiooooooooo"]),
    "laca": ("Lacazette", "artists/lacazette.jpg", ["Kakazette"], ["Lakaaaaaaasetttttttt"]),
    "pasha": ("Pashanim", "artists/pashanim.jpg", ["Kakanim", "Cano030"], ["Paschaaaaaaaaa-Niiiiiim"]),
    "haribo": ("Haribo", "artists/yuyu19.jpg", ["Yuyu"], ["Haaaaarrrriiiiibooooooo"]),
    "kalim": ("Kalim", "artists/kalim.jpg", [], ["Kaaaaaaaaa-liiiiim"]),
    "omar": ("Omar101", "artists/omar101.jpg", [], []),
    "karamel": ("Karamel19", "artists/karamel19.jpg", ["Karmahel19", "Mello"], ["Karaaaaaameeeeeel Eins Neun"]),
    "makko": ("Makko", "artists/makko.jpg", ["Kakko"], []),
    "mucco": ("Mucco", "artists/mucco.jpg", [], ["Muuuuuutschoooooo"]),
    "caney": ("Caney030", "artists/caney030.jpg", [], []),
    "ufo": ("Ufo361", "artists/ufo361.jpg", ["Ufo187"], ["Uuuuuuuufoooooo Drei Sechs Eins"]),
    "luciano": ("Luciano", "artists/luciano.jpg", ["Lucio"], ["BOBOBOBOBOBOOOOOOOOO", "Lussiaaaaaaaaanoooooo"]),
    "samra": ("Samra", "artists/samra.jpg", [], []),
    "souly": ("Souly", "artists/souly.jpg", [], []),
    "zacka": ("Zackavelli", "artists/zackavelli.jpg", ["Masi", "Kakavelli"], []),
}
CORE = ["nizi", "lucio", "laca", "pasha", "haribo", "kalim"]

SONGS = [  # (Titel, Bild, Artist-Key)
    ("CUP", "songs/song-cup.jpg", "laca"), ("FTW", "songs/song-ftw.jpg", "laca"), ("+49", "songs/song-plus49.jpg", "laca"),
    ("Superkraft", "songs/song-superkraft.jpg", "lucio"), ("Wittenbergplatz", "songs/song-wittenbergplatz.jpg", "lucio"),
    ("Hier", "songs/song-hier.jpg", "lucio"), ("Hollywoodreif", "songs/song-hollywoodreif.jpg", "nizi"),
    ("Sommergewitter", "songs/song-sommergewitter.jpg", "pasha"), ("Airwaves", "songs/song-airwaves.jpg", "pasha"),
    ("Kleiner Prinz", "songs/song-kleiner-prinz.jpg", "pasha"), ("16", "songs/song-16.jpg", "kalim"),
]
ALBUMS = [
    ("LID", "albums/album-lid.jpg"), ("101%", "albums/album-101.jpg"), ("Mittendrin", "albums/album-mittendrin.jpg"),
    ("1019", "albums/album-1019.jpg"), ("Doktor", "albums/album-doktor.jpg"), ("Akh & Krach", "albums/album-akh-krach.jpg"),
    ("Free Game", "albums/album-free-game.jpg"), ("Nur für meine Augen", "albums/album-nur-fuer-meine-augen.jpg"),
]

# (gesprochen, Label A, Label B) mit {A}/{B}
ARTIST_Q = [
    ("Würdest du eher ein Jahr nur {A} hören, oder ein Jahr nur {B}?", "1 Jahr nur {A}", "1 Jahr nur {B}"),
    ("Ein Feature mit {A}, oder ein Feature mit {B}?", "Feature mit {A}", "Feature mit {B}"),
    ("Ein Tag mit {A}, oder ein Tag mit {B}?", "1 Tag mit {A}", "1 Tag mit {B}"),
    ("{A} in der ersten Reihe, oder {B} backstage?", "{A} erste Reihe", "{B} backstage"),
    ("{A} als großer Bruder, oder {B} als Mitbewohner?", "{A} als Bruder", "{B} als Mitbewohner"),
    ("Nie wieder {A} hören, oder nie wieder {B} hören?", "Nie wieder {A}", "Nie wieder {B}"),
    ("{A} kocht für dich, oder {B} fährt dich nach Hause?", "{A} kocht", "{B} fährt dich"),
    ("{A} als Lehrer, oder {B} als Fahrlehrer?", "{A} als Lehrer", "{B} als Fahrlehrer"),
]
HOOK_Q = [
    ("Eine Nacht mit {A}, oder nie wieder {B} hören?", "1 Nacht mit {A}", "Nie wieder {B}"),
    ("{A} wird dein Stiefvater, oder {B} dein Klassenlehrer?", "{A} als Stiefvater", "{B} als Klassenlehrer"),
    ("{A} liest deine Chats, oder {B} sieht deinen Suchverlauf?", "{A} liest deine Chats", "{B} sieht deinen Verlauf"),
    ("24 Stunden mit {A} im Fahrstuhl, oder mit {B} im Bällebad?", "{A} im Fahrstuhl", "{B} im Bällebad"),
    ("{A} kommt zu deinem Abiball, oder {B} zu deiner Hochzeit?", "{A} am Abiball", "{B} auf der Hochzeit"),
]
SONG_Q = [
    ("{A} für immer löschen, oder {B} für immer löschen?", "{A} löschen", "{B} löschen"),
    ("{A} auf Dauerschleife, oder {B} auf Dauerschleife?", "{A} auf Repeat", "{B} auf Repeat"),
    ("Nur noch {A} hören, oder nur noch {B}?", "Nur noch {A}", "Nur noch {B}"),
]
ALBUM_Q = [
    ("Nur noch das Album {A} hören, oder nur noch {B}?", "Nur noch {A}", "Nur noch {B}"),
    ("Auf die einsame Insel nimmst du {A} mit, oder {B}?", "Insel: {A}", "Insel: {B}"),
]
FILLER_SLOP = ["Ähhhhhhhhhhhhhh", "Hmmmmmmmmmmmmmm", "Brrrrrrrrrrrrrr", "Wallahiiiiiiiiiii", "Ohhhhhhhh Akhhhhhhhh"]
MID_LEFT = [("Nie wieder duschen", "🚿", "nie wieder duschen"), ("Nie wieder Maka", "🧪", "nie wieder Maka")]
MID_RIGHT = [
    ("Date mit der 3. Person bei „Teilen“", "💘", "ein Date mit der dritten Person, die kommt, wenn du auf Teilen und mehr klickst"),
    ("Mit der 3. Person bei „Teilen“ in den Park", "🌳", "mit der dritten Person aus Teilen und mehr in den Park gehen"),
    ("Der 3. Person bei „Teilen“ „Ich liebe dich“ schreiben", "💌", "der dritten Person aus Teilen und mehr Ich liebe dich schreiben"),
    ("Mit der 3. Person bei „Teilen“ in den Urlaub", "✈️", "mit der dritten Person aus Teilen und mehr in den Urlaub fliegen"),
]
SHARE = [
    ("Teile das Video mit deinen Akhs", "Und teile das Video mit deinen Akhs!"),
    ("Schick das an die 3 sharaflosesten Binnits, die du kennst", "Und schick das an die 3 sharaflosesten Binnits, die du kennst!"),
] + [(f"Schick das an die 3 größten {w}, die du kennst", f"Und schick das an die 3 größten {w}, die du kennst!")
     for w in ["Gooner", "Stoner", "Ottos", "Talahons"]]


def pct(rng):
    r = rng.random()
    if r < 0.4:
        x = rng.randint(1, 9)
    elif r < 0.7:
        x = rng.choice([44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 55, 56])
    else:
        x = rng.randint(15, 35)
    return [x, 100 - x] if rng.random() < 0.5 else [100 - x, x]


ALBUM_ARTISTS = {"LID": ["laca"], "101%": ["lucio"], "Mittendrin": ["lucio"], "1019": ["lucio", "nizi"], "Doktor": ["nizi"],
                 "Akh & Krach": ["nizi", "haribo"], "Free Game": ["kalim"], "Nur für meine Augen": ["kalim"]}
SONG_ARTIST = {t: k for t, _, k in SONGS}
IMG = {v[1]: ("a", k) for k, v in ARTISTS.items()}
IMG.update({img: ("s", t) for t, img, _ in SONGS})
IMG.update({img: ("al", t) for t, img in ALBUMS})
MAX_PAIR = 4      # gleiche Paarung hoechstens 4x ueber alle Videos
MAX_PER_VIDEO = 2  # jeder Rapper hoechstens 2x pro Video


def label_pattern(label):
    names = sorted({n for v in ARTISTS.values() for n in [v[0]] + v[2]} | {t for t, _, _ in SONGS} | {t for t, _ in ALBUMS},
                   key=len, reverse=True)
    for n in names:
        if n in label:
            return label.replace(n, "{}", 1)
    return label


class State:
    def __init__(self):
        self.pairs = Counter()
        self.exact = set()

    def key(self, kind, x, y):
        return (kind,) + tuple(sorted((x, y)))

    def add_existing(self, v):
        for q in [v.get("hook")] + v["questions"]:
            if not q or q.get("type") == "mid":
                continue
            a, b = IMG.get(q["a"].get("img")), IMG.get(q["b"].get("img"))
            if not a or not b:
                continue
            k = self.key(a[0], a[1], b[1])
            self.pairs[k] += 1
            self.exact.add((k, label_pattern(q["a"]["label"])))


def make(n, st):
    for attempt in range(400):
        v = try_make(n, st, random.Random(1000 * attempt + n))
        if v:
            return v
    return None


def try_make(n, st, rng):
    per = Counter()
    used = []  # (key, pattern) die dieses Video belegt

    def ok_people(keys):
        c = Counter(keys)
        return all(per[k] + c[k] <= MAX_PER_VIDEO for k in c)

    def take(kind, x, y, tpl_a, people):
        k = st.key(kind, x, y)
        pat = tpl_a.replace("{A}", "{}").replace("{B}", "{}")
        if st.pairs[k] + sum(1 for u in used if u[0] == k) >= MAX_PAIR:
            return False
        if (k, pat) in st.exact or any(u == (k, pat) for u in used) or any(u[0] == k for u in used):
            return False
        if not ok_people(people):
            return False
        for p in people:
            per[p] += 1
        used.append((k, pat))
        return True

    def pick_artist(tpls):
        keys = list(ARTISTS)
        for _ in range(200):
            a = rng.choice(CORE) if rng.random() < 0.6 else rng.choice(keys)
            b = rng.choice([k for k in keys if k != a])
            say, la, lb = rng.choice(tpls)
            # seltene Paarungen bevorzugen
            if st.pairs[st.key("a", a, b)] >= 2 and rng.random() < 0.6:
                continue
            if take("a", a, b, la, [a, b]):
                return {"kind": "artist", "keys": [a, b], "say": say, "la": la, "lb": lb,
                        "a": {"img": ARTISTS[a][1]}, "b": {"img": ARTISTS[b][1]}}
        return None

    def pick_song():
        for _ in range(200):
            x, y = rng.sample(SONGS, 2)
            say, la, lb = rng.choice(SONG_Q)
            ppl = [x[2], y[2]]
            if take("s", x[0], y[0], la, ppl):
                return {"kind": "song", "names": [x[0], y[0]], "say": say, "la": la, "lb": lb, "a": {"img": x[1]}, "b": {"img": y[1]}}
        return None

    def pick_album():
        for _ in range(200):
            x, y = rng.sample(ALBUMS, 2)
            say, la, lb = rng.choice(ALBUM_Q)
            ppl = ALBUM_ARTISTS[x[0]] + ALBUM_ARTISTS[y[0]]
            if take("al", x[0], y[0], la, ppl):
                return {"kind": "album", "names": [x[0], y[0]], "say": say, "la": la, "lb": lb, "a": {"img": x[1]}, "b": {"img": y[1]}}
        return None

    hook = pick_artist(HOOK_Q)
    qs = [pick_artist(ARTIST_Q) for _ in range(4)] + [pick_song(), pick_song(), pick_album()]
    if not hook or not all(qs):
        return None
    rng.shuffle(qs)

    cands = [(q, i) for q in [hook] + qs if q["kind"] == "artist" for i in (0, 1) if ARTISTS[q["keys"][i]][2]]
    if not cands:
        return None
    nick_q, nick_i = rng.choice(cands)
    nick_q["nick"] = (nick_i, rng.choice(ARTISTS[nick_q["keys"][nick_i]][2]))

    slop_slots = [(q, i) for q in qs if q["kind"] == "artist" for i in (0, 1)
                  if ARTISTS[q["keys"][i]][3] and not (q.get("nick") and q["nick"][0] == i)]
    rng.shuffle(slop_slots)
    slop_slots.sort(key=lambda s: 0 if s[0]["keys"][s[1]] in ("lucio", "luciano") else 1)
    for q, i in slop_slots[:rng.choice([2, 2, 3])]:
        q.setdefault("slop", {})[i] = rng.choice(ARTISTS[q["keys"][i]][3])
    have = sum(len(q.get("slop", {})) for q in qs)
    for q in rng.sample(qs, max(0, 2 - have)):
        q["filler"] = rng.choice(FILLER_SLOP)

    def render(q):
        if q["kind"] == "artist":
            names = [ARTISTS[k][0] for k in q["keys"]]
            if q.get("nick"):
                names[q["nick"][0]] = q["nick"][1]
            spoken = [f"[[{q['slop'][i]}]]" if i in q.get("slop", {}) else names[i] for i in (0, 1)]
        else:
            names = spoken = q["names"]
        say = q["say"].format(A=spoken[0], B=spoken[1])
        if q.get("filler") and not say.startswith("[["):
            say = f"[[{q['filler']}]], " + say[0].lower() + say[1:]
        p = pct(rng)
        out = {"say": say, "a": {"label": q["la"].format(A=names[0], B=names[1]), "img": q["a"]["img"]},
               "b": {"label": q["lb"].format(A=names[0], B=names[1]), "img": q["b"]["img"]}, "pct": p}
        if q["kind"] == "artist":
            win = q["keys"][0] if p[0] >= p[1] else q["keys"][1]
            if win == "haribo" and rng.random() < 0.6:
                out["winSay"] = "Ohne Finger, Akh!"
        return out

    left, right = rng.choice(MID_LEFT), rng.choice(MID_RIGHT)
    mid = {"type": "mid", "say": f"Kurze Pause. {left[2][0].upper() + left[2][1:]}, oder {right[2]}?",
           "a": {"label": left[0], "emoji": left[1]}, "b": {"label": right[0], "emoji": right[1]}, "pct": pct(rng)}
    questions = [render(q) for q in qs]
    questions.insert(4, mid)
    h = render(hook)
    h["type"] = "hook"
    share = rng.choice(SHARE)
    for k, pat in used:
        st.pairs[k] += 1
        st.exact.add((k, pat))
    return {
        "id": f"a{n:02d}", "channel": "A", "handle": "@akhmachtkrach19", "hook": h, "questions": questions,
        "outro": {"say": "Wie oft lagst du richtig, Akh? Schreibs in die Kommentare!", "title": "WIE OFT LAGST DU RICHTIG, AKH?",
                  "sub": "Schreibs in die Kommentare", "share": share[0], "shareSay": share[1]},
    }


if __name__ == "__main__":
    # python3 scripts/generate.py <erstes neues> <letztes>  (alle Videos davor bleiben fest und zaehlen mit)
    a, b = int(sys.argv[1]), int(sys.argv[2])
    st = State()
    for f in sorted(OUT.glob("a*.json")):
        if int(f.stem[1:]) < a:
            st.add_existing(json.loads(f.read_text(encoding="utf-8")))
    made = 0
    for n in range(a, b + 1):
        v = make(n, st)
        if not v:
            print(f"a{n:02d}: keine Kombination mehr moeglich, stoppe")
            break
        (OUT / f"{v['id']}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
        made += 1
    for f in OUT.glob("a*.json"):
        if int(f.stem[1:]) >= a + made:
            f.unlink()
    print(f"{made} Skripte geschrieben")
