"""Schreibt die Video-Skripte fuer Kanal A (content/videos/aNN.json).

Regeln (von Jakob):
- pro Video genau 1 Spitzname/Fake-Name
- pro Video mindestens 2 weirde TTS-Effekte (in [[...]], werden nicht umgeschrieben)
- Haribo gewinnt -> manchmal "Ohne Finger, Akh!" nach der Aufloesung
- Prozente teils extrem (1/99), teils knapp
Aufruf: python3 scripts/generate.py 2 50
"""
import json, random, sys
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


def make(n):
    rng = random.Random(1000 + n)
    used_pairs = set()
    qs = []

    def artist_pair():
        while True:
            a = rng.choice(CORE) if rng.random() < 0.65 else rng.choice(list(ARTISTS))
            b = rng.choice([k for k in ARTISTS if k != a])
            if frozenset((a, b)) not in used_pairs:
                used_pairs.add(frozenset((a, b)))
                return a, b

    def artist_q(tpls):
        a, b = artist_pair()
        say, la, lb = rng.choice(tpls)
        return {"kind": "artist", "keys": [a, b], "say": say, "la": la, "lb": lb,
                "a": {"img": ARTISTS[a][1]}, "b": {"img": ARTISTS[b][1]}}

    hook = artist_q(HOOK_Q)
    for _ in range(4):
        qs.append(artist_q(ARTIST_Q))
    s1, s2 = rng.sample(SONGS, 2)
    s3, s4 = rng.sample([s for s in SONGS if s not in (s1, s2)], 2)
    for x, y in ((s1, s2), (s3, s4)):
        say, la, lb = rng.choice(SONG_Q)
        qs.append({"kind": "song", "names": [x[0], y[0]], "say": say, "la": la, "lb": lb, "a": {"img": x[1]}, "b": {"img": y[1]}})
    x, y = rng.sample(ALBUMS, 2)
    say, la, lb = rng.choice(ALBUM_Q)
    qs.append({"kind": "album", "names": [x[0], y[0]], "say": say, "la": la, "lb": lb, "a": {"img": x[1]}, "b": {"img": y[1]}})
    rng.shuffle(qs)

    # 1 Spitzname pro Video
    cands = [(q, i) for q in [hook] + qs if q["kind"] == "artist" for i in (0, 1) if ARTISTS[q["keys"][i]][2]]
    nick_q, nick_i = rng.choice(cands)
    nick_q["nick"] = (nick_i, rng.choice(ARTISTS[nick_q["keys"][nick_i]][2]))

    # mind. 2 TTS-Effekte: bevorzugt Namen mit Slop (Lucio oft), sonst Fueller
    slop_slots = [(q, i) for q in qs if q["kind"] == "artist" for i in (0, 1)
                  if ARTISTS[q["keys"][i]][3] and not (q.get("nick") and q["nick"][0] == i)]
    rng.shuffle(slop_slots)
    slop_slots.sort(key=lambda s: 0 if s[0]["keys"][s[1]] in ("lucio", "luciano") else 1)
    want = rng.choice([2, 2, 3])
    for q, i in slop_slots[:want]:
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
        if q.get("filler"):
            say = f"[[{q['filler']}]], " + say[0].lower() + say[1:] if not say.startswith("[[") else say
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
    return {
        "id": f"a{n:02d}", "channel": "A", "handle": "@akhmachtkrach19", "hook": h, "questions": questions,
        "outro": {"say": "Wie oft lagst du richtig, Akh? Schreibs in die Kommentare!", "title": "WIE OFT LAGST DU RICHTIG, AKH?",
                  "sub": "Schreibs in die Kommentare", "share": share[0], "shareSay": share[1]},
    }


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for n in range(a, b + 1):
        v = make(n)
        (OUT / f"{v['id']}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print(f"{b - a + 1} Skripte geschrieben")
