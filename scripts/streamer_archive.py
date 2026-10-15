"""Baut das Streamer-Archiv fuer Kanal B aus den Recherche-Rohdaten.

Eingabe: content/streamer/raw/*.json (Recherche Oktober 2026)
Ausgabe: content/streamer/archive.json (pro Streamer: Steckbrief, Spitznamen, Material)

Material ist Inspiration, keine fertigen Witze. Kategorien:
  zitat, gag, moment, look, sound, habit, meme
Aufruf: python3 scripts/streamer_archive.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "content" / "streamer" / "raw"
OUT = ROOT / "content" / "streamer" / "archive.json"

CORE = ["papaplatte", "montanablack", "knossi", "trymacs", "unge", "rewinside",
        "handofblood", "gronkh", "eliasn97", "sidneyeweka", "mckytv", "reved"]
ALIAS = {"dagi_bee": "dagibee", "julien_bam": "julienbam"}
SKIP_MEMES = {"Talahon"}  # Stereotyp, steht auf der Avoid-Liste
SKIP_PEOPLE = {"apored"}  # komplett auf der Avoid-Liste

GAG_CAT = {"catchphrase": "zitat", "emote": "zitat", "running_gag": "gag", "insider": "gag",
           "format": "moment", "trait": "habit"}
TRAIT_CAT = {"sound": "sound", "look_now": "look", "look_old": "look", "habit": "habit",
             "prop": "habit", "era": "look"}


def load(name):
    return json.load(open(RAW / f"{name}.json", encoding="utf-8"))


def key(k):
    return ALIAS.get(k, k)


def main():
    cast = load("cast")
    nick_v = load("nicknames_verified")["streamers"]
    nick_g = load("nicknames")
    people = {}

    def person(k, name=None):
        k = key(k)
        if k not in people:
            people[k] = {"key": k, "name": name or k, "core": k in CORE, "items": []}
        return people[k]

    for s in cast["streamers"]:
        p = person(s["key"], s["name"])
        p.update({kk: s.get(kk) for kk in ("vibe", "followers", "active", "platforms", "crew", "rivals",
                                           "hugo_frequency", "hugo_evidence", "avatar_source")})
        p["cast_sources"] = s.get("source_urls", [])

    for k, v in nick_v.items():
        p = person(k, v.get("display"))
        p["real_name"] = v.get("real_name")
        p["nicknames"] = v.get("nicknames", [])
        p["name_origin"] = v.get("name_origin")
        p["pronunciation"] = v.get("pronunciation")
    for k, v in nick_g["streamers"].items():
        p = person(k, v.get("display"))
        p["invented_names"] = v.get("fake_names", [])  # erfunden, nur als Anregung
        p["slop"] = v.get("slop", [])

    def add(keys, item):
        for k in keys or ["_allgemein"]:
            person(k)["items"].append(item)

    for f in ("gags_1", "gags_2"):
        for e in load(f)["entries"]:
            add(e["streamers"], {"id": e["id"], "cat": GAG_CAT.get(e["type"], "gag"), "label": e["title"],
                                 "quote": e.get("quote"), "detail": e.get("context"), "year": e.get("year"),
                                 "image": e.get("image_hint"), "sources": e.get("source_urls", []),
                                 "conf": e.get("confidence"), "with": e["streamers"]})
    for e in load("moments")["entries"]:
        add(e["streamers"], {"id": e["id"], "cat": "moment", "sub": e["type"], "label": e["title"],
                             "detail": e.get("context"), "year": e.get("year"), "image": e.get("image_hint"),
                             "sources": e.get("source_urls", []), "conf": e.get("confidence"),
                             "with": e["streamers"]})
    for e in load("traits")["entries"]:
        add([e["streamer"]], {"id": e["id"], "cat": TRAIT_CAT.get(e["kind"], "habit"), "sub": e["kind"],
                              "label": e["label"], "detail": e.get("detail"), "year": e.get("years"),
                              "image": e.get("image_lookup"), "sources": e.get("source_urls", []),
                              "conf": e.get("confidence"), "with": [key(e["streamer"])]})
    memes = load("memes")
    for e in memes["entries"]:
        if e["streamer_link"] and e["title"] not in SKIP_MEMES:
            add(e["streamer_link"], {"id": e["id"], "cat": "meme", "label": e["title"], "detail": e.get("meaning"),
                                     "year": e.get("year"), "jugendwort": e.get("jugendwort"),
                                     "image": e.get("image_hint"), "sources": e.get("source_urls", []),
                                     "conf": e.get("confidence"), "with": e["streamer_link"]})

    avoid = []
    for f in ("gags_1", "gags_2"):
        avoid += [{"who": a.get("streamer"), "topic": a.get("topic"), "why": a.get("why")} for a in load(f)["avoid"]]
    avoid += [{"who": None, "topic": a.get("topic"), "why": a.get("reason")} for a in load("moments")["avoid"]]
    avoid += [{"who": None, "topic": a if isinstance(a, str) else a.get("topic"), "why": None if isinstance(a, str) else a.get("why")}
              for a in load("traits")["avoid"]]
    avoid += [{"who": None, "topic": a.get("title"), "why": a.get("reason")} for a in memes["avoid"]]

    order = {k: i for i, k in enumerate(CORE)}
    ppl = sorted(people.values(), key=lambda p: (order.get(p["key"], 99), -len(p["items"]), p["key"]))
    ppl = [p for p in ppl if p["key"] not in SKIP_PEOPLE and (p["items"] or p["core"] or p.get("vibe"))]
    out = {"_info": "Inspiration fuer Kanal B (Streamer). Keine fertigen Witze. conf=low heisst: vor Nutzung pruefen.",
           "streamers": ppl, "pairings": cast["pairings"], "filler_slop": nick_g["filler_slop"], "avoid": avoid}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(ppl)} Personen, {sum(len(p['items']) for p in ppl)} Eintraege, {len(avoid)} Avoid -> {OUT}")


if __name__ == "__main__":
    main()
