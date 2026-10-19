"""Schreibt die Test-Skripte fuer den Geld-Kanal (content/videos/gNN.json).

g01-g03: belehrend (Umfrage, dann Aufloesung fuer beide Seiten; Mehrheit liegt bewusst falsch)
g04-g06: Umfrage-Format wie Kanal A
Stimmen-Test: g01, g04, g05 Adam (Standard) / g02, g03, g06 Brian (ernster, langsamer)
Aufruf: python3 scripts/generate_geld.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "content" / "videos"
ADAM = None
BRIAN = {"name": "Brian (ernst)", "id": "nPczCjzI2devNBz1zQrb", "speed": 1.06, "stability": 0.85, "style": 0}

def o(label, emoji): return {"label": label, "emoji": emoji}
def q(say, a, b, pct, explain=None):
    d = {"say": say, "a": o(*a), "b": o(*b), "pct": pct}
    if explain:
        (fa, sa), (fb, sb), best, win = explain
        d["explain"] = {"a": {"fact": fa, "say": sa}, "b": {"fact": fb, "say": sb}, "best": best, "winSay": win}
    return d
def mid(say, a, b, pct): return {"type": "mid", **q("Kurze Pause. " + say, a, b, pct)}

OUTRO_QUIZ = {"say": "Wie oft lagst du richtig? Schreibs in die Kommentare!", "title": "WIE OFT LAGST DU RICHTIG?",
              "sub": "Schreibs in die Kommentare", "share": "Schick das an jemanden, der jeden Monat pleite ist",
              "shareSay": "Und schick das an jemanden, der jeden Monat pleite ist!"}
OUTRO_POLL = {"say": "Was hättest du gewählt? Schreibs in die Kommentare!", "title": "WAS HÄTTEST DU GEWÄHLT?",
              "sub": "Schreibs in die Kommentare", "share": "Schick das an deinen Kumpel mit dem Dispo",
              "shareSay": "Und schick das an deinen Kumpel mit dem Dispo!"}

V = {}
# ---------- belehrend: Umfrage, dann Aufloesung fuer beide Seiten (Mehrheit liegt bewusst falsch) ----------
V["g01"] = dict(format="quiz", voice=ADAM,
  claim={"title": "NUR 15%", "sub": "ANTWORTEN RICHTIG", "say": "Nur 15 Prozent beantworten alle drei richtig!"},
  questions=[
    q("1 Million Euro sofort, oder 5.000 Euro im Monat für immer?", ("1 Mio. € sofort", "💰"), ("5.000 € / Monat", "📅"), [31, 69],
      (("Bei ~7 % Rendite: ca. 70.000 € pro Jahr. Die Million bleibt.", "Die Million bringt bei historisch rund 7 Prozent im Schnitt etwa 70.000 Euro im Jahr. Und die Million bleibt dir."),
       ("5.000 € im Monat = nur 60.000 € im Jahr", "Die 5.000 Euro im Monat sind nur 60.000 Euro im Jahr."),
       "a", "Die Million gewinnt. Und die kannst du sogar vererben.")),
    q("100.000 Euro sofort, oder 1 Cent, der sich 30 Tage lang jeden Tag verdoppelt?", ("100.000 € sofort", "💶"), ("1 Cent × 2, 30 Tage", "🪙"), [72, 28],
      (("100.000 €, sofort auf dem Konto", "Die 100.000 Euro hast du sofort."),
       ("Tag 20: 5.243 €\nTag 30: 5,37 Mio. €", "Der Cent ist an Tag 20 erst bei 5.243 Euro. Aber an Tag 30 bei über 5,3 Millionen."),
       "b", "Der Cent gewinnt. Das ist exponentielles Wachstum.")),
    mid("Nie wieder Lieferando, oder nie wieder Netflix?", ("Nie wieder Lieferando", "🍕"), ("Nie wieder Netflix", "📺"), [44, 56]),
    q("Ab 20 jeden Monat 100 Euro anlegen, oder ab 40 jeden Monat 300 Euro?", ("Ab 20: 100 € / Monat", "🧑"), ("Ab 40: 300 € / Monat", "🧔"), [38, 62],
      (("Mit 65: ca. 379.000 €\n(eingezahlt: 54.000 €)", "Bei 7 Prozent im Jahr hast du mit 65 rund 379.000 Euro. Eingezahlt hast du nur 54.000."),
       ("Mit 65: ca. 243.000 €\n(eingezahlt: 90.000 €)", "Ab 40 sind es nur rund 243.000 Euro. Obwohl du 90.000 eingezahlt hast."),
       "a", "Früh anfangen schlägt viel einzahlen.")),
  ], outro=OUTRO_QUIZ)

V["g02"] = dict(format="quiz", voice=BRIAN,
  claim={"title": "80%", "sub": "ANTWORTEN FALSCH", "say": "80 Prozent antworten hier falsch. Du auch?"},
  questions=[
    q("Neuwagen für 30.000 Euro, oder Gebrauchtwagen für 15.000 und den Rest anlegen?", ("Neuwagen 30.000 €", "🚗"), ("Gebraucht + 15.000 € anlegen", "🚙"), [58, 42],
      (("Verliert in 3 Jahren oft ~40 % Wert = ca. 12.000 €", "Ein Neuwagen verliert in den ersten drei Jahren oft rund 40 Prozent an Wert. Das sind 12.000 Euro."),
       ("15.000 € bei 7 % → ca. 29.500 € nach 10 Jahren", "Die 15.000 Euro können bei 7 Prozent in zehn Jahren auf rund 29.500 Euro wachsen."),
       "b", "Gebraucht kaufen und anlegen gewinnt.")),
    q("Ein Auto für 299 Euro im Monat leasen, oder ein Auto für 10.000 Euro bar kaufen?", ("Leasing 299 € / Monat", "📝"), ("10.000 € bar", "💵"), [63, 37],
      (("3 Jahre: 10.764 € gezahlt. Auto gehört dir nicht.", "Beim Leasing zahlst du in drei Jahren über 10.700 Euro. Und danach gehört dir das Auto nicht."),
       ("Auto gehört dir und ist nach 3 Jahren noch was wert", "Bar gekauft gehört dir das Auto. Und nach drei Jahren kannst du es noch verkaufen."),
       "b", "Bar kaufen gewinnt. Wenn du das Geld hast.")),
    mid("Nie wieder Kaffee, oder nie wieder Spotify?", ("Nie wieder Kaffee", "☕"), ("Nie wieder Spotify", "🎧"), [61, 39]),
    q("Jede Woche 10 Euro Lotto spielen, oder jede Woche 10 Euro in einen ETF?", ("10 € / Woche Lotto", "🎰"), ("10 € / Woche ETF", "📈"), [55, 45],
      (("Jackpot-Chance: 1 zu 140 Millionen", "Die Chance auf den Lotto-Jackpot liegt bei etwa eins zu 140 Millionen."),
       ("40 Jahre bei 7 % → ca. 114.000 €", "Im ETF werden aus 10 Euro pro Woche in 40 Jahren bei 7 Prozent rund 114.000 Euro."),
       "b", "Der ETF gewinnt. Fast immer.")),
  ], outro=OUTRO_QUIZ)

V["g03"] = dict(format="quiz", voice=BRIAN,
  claim={"title": "NUR 1 VON 10", "sub": "SCHAFFT ALLE 3", "say": "Nur einer von zehn schafft alle drei!"},
  questions=[
    q("Einen Abend die Steuererklärung machen, oder einen Abend Netflix?", ("Steuererklärung", "🧾"), ("Netflix-Abend", "🍿"), [41, 59],
      (("Im Schnitt rund 1.000 € Erstattung", "Wer die Steuererklärung macht, bekommt im Schnitt rund 1.000 Euro zurück."),
       ("Kostet dich Geld, bringt dir keins", "Netflix kostet dich Geld, statt dir welches zu bringen."),
       "a", "Steuererklärung gewinnt. Danach kannst du ja Netflix schauen.")),
    q("200 Euro mehr Gehalt im Monat, oder einmalig 2.000 Euro Bonus?", ("+200 € Gehalt / Monat", "📈"), ("2.000 € Bonus", "🎁"), [34, 66],
      (("2.400 € im Jahr. Jedes Jahr.", "200 Euro mehr im Monat sind 2.400 Euro im Jahr. Jedes Jahr. Und jede Gehaltserhöhung baut darauf auf."),
       ("Einmal 2.000 €, dann vorbei", "Der Bonus kommt genau einmal. Dann ist er weg."),
       "a", "Mehr Gehalt gewinnt. Schon nach einem Jahr.")),
    mid("Nie wieder Kino, oder nie wieder Konzerte?", ("Nie wieder Kino", "🎬"), ("Nie wieder Konzerte", "🎤"), [64, 36]),
    q("5.000 Euro Dispo abbezahlen, oder die 5.000 Euro in einen ETF stecken?", ("Dispo abbezahlen", "🏦"), ("5.000 € in ETF", "📊"), [37, 63],
      (("Dispo kostet oft über 10 % Zinsen. Garantiert.", "Der Dispo kostet dich oft über 10 Prozent Zinsen. Und zwar garantiert."),
       ("ETF: im Schnitt ~7 %, ohne Garantie", "Der ETF bringt im Schnitt vielleicht 7 Prozent. Aber ohne Garantie."),
       "a", "Schulden zuerst. Immer.")),
  ], outro=OUTRO_QUIZ)

# ---------- Umfrage-Format wie Kanal A, nur Prozente ----------
V["g04"] = dict(format="poll", voice=ADAM,
  claim={"title": "90%", "sub": "WÄHLEN FALSCH", "say": "90 Prozent wählen hier falsch!"},
  questions=[
    q("10.000 Euro sofort, oder 1.000 Euro jeden Monat für ein Jahr?", ("10.000 € sofort", "💶"), ("1.000 € × 12 Monate", "📅"), [61, 39]),
    q("Doppeltes Gehalt mit 2 Wochen Urlaub, oder normales Gehalt mit 3 Monaten Urlaub?", ("Doppeltes Gehalt", "💰"), ("3 Monate Urlaub", "🏖️"), [44, 56]),
    q("4-Tage-Woche mit 80 Prozent Gehalt, oder 5 Tage mit vollem Gehalt?", ("4 Tage, 80 %", "🗓️"), ("5 Tage, 100 %", "💼"), [73, 27]),
    q("Eigentumswohnung in Leipzig, oder Mietwohnung in München?", ("Eigentum Leipzig", "🏠"), ("Miete München", "🏙️"), [66, 34]),
    mid("Nie wieder Döner, oder nie wieder Pizza?", ("Nie wieder Döner", "🥙"), ("Nie wieder Pizza", "🍕"), [47, 53]),
    q("Nie wieder Steuern zahlen, oder nie wieder Miete zahlen?", ("Nie wieder Steuern", "🧾"), ("Nie wieder Miete", "🔑"), [48, 52]),
    q("Mit 25 schuldenfrei, oder mit 25 eine Weltreise auf Kredit?", ("Schuldenfrei mit 25", "✅"), ("Weltreise auf Kredit", "✈️"), [81, 19]),
    q("Dein Gehalt öffentlich für alle, oder dein Kontostand öffentlich für alle?", ("Gehalt öffentlich", "📄"), ("Kontostand öffentlich", "🏦"), [57, 43]),
  ], outro=OUTRO_POLL)

V["g05"] = dict(format="poll", voice=ADAM,
  claim={"title": "NUR 12%", "sub": "LIEGEN RICHTIG", "say": "Nur 12 Prozent liegen hier richtig!"},
  questions=[
    q("500.000 Euro sofort, oder 1 Euro, der sich 20 Tage lang jeden Tag verdoppelt?", ("500.000 € sofort", "💰"), ("1 € × 2, 20 Tage", "🪙"), [38, 62]),
    q("Traumjob mit 2.500 netto, oder Hassjob mit 6.000 netto?", ("Traumjob 2.500 €", "😍"), ("Hassjob 6.000 €", "😩"), [52, 48]),
    q("Lotto-Jackpot mit 70, oder 1 Million mit 25?", ("Jackpot mit 70", "👴"), ("1 Mio. mit 25", "🧑"), [9, 91]),
    q("Ein Haus in der Pampa erben, oder 200.000 Euro bar?", ("Haus in der Pampa", "🏡"), ("200.000 € bar", "💵"), [35, 65]),
    mid("Ein Jahr kein Handy, oder ein Jahr kein Urlaub?", ("1 Jahr kein Handy", "📱"), ("1 Jahr kein Urlaub", "🏝️"), [39, 61]),
    q("Chef mit 60 Stunden pro Woche, oder Angestellter mit 35 Stunden?", ("Chef, 60 h", "👔"), ("Angestellter, 35 h", "🧑‍💻"), [46, 54]),
    q("Für immer kostenlos Bahn fahren, oder für immer kostenlos tanken?", ("Gratis Bahn", "🚆"), ("Gratis tanken", "⛽"), [29, 71]),
    q("Ein Jahr lang alles bezahlt bekommen, oder 50.000 Euro bar?", ("1 Jahr alles bezahlt", "🎁"), ("50.000 € bar", "💶"), [64, 36]),
  ], outro=OUTRO_POLL)

V["g06"] = dict(format="poll", voice=BRIAN,
  claim={"title": "80%", "sub": "ANTWORTEN FALSCH", "say": "80 Prozent antworten hier falsch!"},
  questions=[
    q("Mit 30 in Rente mit 2.000 Euro im Monat, oder mit 67 mit 6.000 Euro?", ("Rente mit 30, 2.000 €", "🏖️"), ("Rente mit 67, 6.000 €", "👴"), [77, 23]),
    q("Reich und einsam, oder pleite mit den besten Freunden?", ("Reich und einsam", "💎"), ("Pleite mit Freunden", "🫂"), [42, 58]),
    q("Ein Jahr ohne Handy für 50.000 Euro, oder ein Jahr ohne Auto für 20.000 Euro?", ("Ohne Handy: 50.000 €", "📵"), ("Ohne Auto: 20.000 €", "🚗"), [68, 32]),
    q("Nie wieder Online-Shopping, oder nie wieder Essen bestellen?", ("Kein Online-Shopping", "📦"), ("Kein Essen bestellen", "🛵"), [53, 47]),
    mid("Nie wieder Gym, oder nie wieder Fast Food?", ("Nie wieder Gym", "🏋️"), ("Nie wieder Fast Food", "🍔"), [38, 62]),
    q("100.000 Euro jetzt, oder 1 Million mit 60?", ("100.000 € jetzt", "⚡"), ("1 Mio. mit 60", "⏳"), [55, 45]),
    q("Selbstständig mit unsicherem Einkommen, oder Beamter mit sicherem Gehalt?", ("Selbstständig", "🚀"), ("Beamter", "🏛️"), [47, 53]),
    q("Bei den Eltern wohnen und keine Miete, oder eigene Wohnung und alles selbst zahlen?", ("Bei den Eltern", "🏡"), ("Eigene Wohnung", "🔑"), [31, 69]),
  ], outro=OUTRO_POLL)

# ---------- Experimente g07-g10: TTS-Bug in den ersten 2 Sekunden, neue Formate ----------
MYTH, FACT = ("MYTHOS", "🧢"), ("FAKT", "✅")
def myth(statement, pct, best, fact, say, win):
    """Aussage oben, unten MYTHOS/FAKT. Aufloesung nur auf der richtigen Seite."""
    return {"say": statement + " Mythos, oder Fakt?", "statement": statement, "a": o(*MYTH), "b": o(*FACT), "pct": pct,
            "explain": {best: {"fact": fact, "say": say}, "best": best, "winSay": win, "stamps": ["RICHTIG", "FALSCH"],
                        "note": "Vereinfacht. Keine Steuer- oder Anlageberatung."}}

V["g07"] = dict(format="quiz", voice=ADAM,
  claim={"title": "NUR 9%", "sub": "RECHNEN RICHTIG", "say": "Nur 9 Prozent rechnen hier richtig!", "glitch": "stutter"},
  questions=[
    q("Erst 20 Prozent Rabatt und dann nochmal 20 Prozent, oder direkt 40 Prozent Rabatt?", ("2 × 20 % Rabatt", "🏷️"), ("40 % Rabatt", "💥"), [64, 36],
      (("100 € → 80 € → 64 €\n= nur 36 % gespart", "Zweimal 20 Prozent sind nur 36 Prozent."),
       ("100 € → 60 €\n= 40 % gespart", "Direkt 40 Prozent sind 40 Prozent."),
       "b", "Die 40 Prozent gewinnen.")),
    q("Deine Aktie steigt um 50 Prozent und fällt dann um 50 Prozent. Plus minus null, oder Verlust?", ("Plus minus null", "⚖️"), ("Verlust", "📉"), [71, 29],
      (("Klingt logisch, ist aber falsch", "Klingt logisch. Ist aber falsch."),
       ("100 € → 150 € → 75 €\n= 25 % Verlust", "Aus 100 werden 150. Dann nur noch 75. Also 25 Prozent Verlust."),
       "b", "Verlust. Prozente rechnen immer vom neuen Wert.")),
    q("Drei für zwei, oder 30 Prozent Rabatt auf alles?", ("3 für 2", "🛒"), ("30 % Rabatt", "🏷️"), [41, 59],
      (("Du zahlst 2 von 3\n= 33 % gespart", "Drei für zwei sind 33 Prozent Rabatt."),
       ("Nur 30 % gespart", "30 Prozent bleiben 30 Prozent."),
       "a", "Drei für zwei gewinnt. Wenn du alle drei brauchst.")),
  ], outro=OUTRO_QUIZ)

V["g08"] = dict(format="myth", voice=BRIAN,
  claim={"title": "95%", "sub": "GLAUBEN DAS", "say": "95 Prozent glauben das!", "glitch": "slowmo"},
  questions=[
    myth("Mit einer Gehaltserhöhung kannst du netto weniger haben.", [38, 62], "a",
         "Nur der zusätzliche Teil wird höher besteuert. Netto bleibt mehr.",
         "Bei der Lohnsteuer wird nur der zusätzliche Teil höher besteuert. Netto bleibt also trotzdem mehr übrig.", "Mythos!"),
    myth("Geld auf dem Girokonto verliert bei Inflation an Wert.", [57, 43], "b",
         "Bei 2 % Inflation sind 10.000 € nach 10 Jahren nur noch ca. 8.200 € wert.",
         "Bei 2 Prozent Inflation kaufst du mit 10.000 Euro nach zehn Jahren nur noch so viel wie heute mit 8.200.", "Fakt!"),
    myth("Trinkgeld musst du als Angestellter versteuern.", [39, 61], "a",
         "Freiwilliges Trinkgeld von Gästen ist für Angestellte steuerfrei.",
         "Freiwilliges Trinkgeld von Gästen ist für Angestellte in Deutschland steuerfrei.", "Mythos!"),
  ], outro=OUTRO_QUIZ)

V["g09"] = dict(format="speedrun", voice=ADAM, pace={"timer": 60, "hold": 30},
  claim={"title": "11 FRAGEN", "sub": "2 SEKUNDEN", "say": "11 Fragen. Nur 2 Sekunden. Los!", "glitch": "chipmunk"},
  questions=[
    q("Reich mit 30, oder glücklich mit 30?", ("Reich mit 30", "💰"), ("Glücklich mit 30", "😊"), [44, 56]),
    q("Nie wieder Miete, oder nie wieder Steuern?", ("Nie wieder Miete", "🔑"), ("Nie wieder Steuern", "🧾"), [52, 48]),
    q("1.000 Euro jetzt, oder 2.000 in einem Jahr?", ("1.000 € jetzt", "⚡"), ("2.000 € in 1 Jahr", "⏳"), [37, 63]),
    q("Gratis Essen für immer, oder gratis Wohnen für immer?", ("Gratis Essen", "🍔"), ("Gratis Wohnen", "🏠"), [22, 78]),
    q("Lotto-Gewinn, oder Traumjob?", ("Lotto-Gewinn", "🎰"), ("Traumjob", "💼"), [69, 31]),
    q("Bitcoin, oder Gold?", ("Bitcoin", "🪙"), ("Gold", "🥇"), [58, 42]),
    q("Nur Bargeld, oder nur Karte?", ("Nur Bargeld", "💵"), ("Nur Karte", "💳"), [35, 65]),
    q("Erben, oder selbst verdienen?", ("Erben", "🎁"), ("Selbst verdienen", "💪"), [61, 39]),
    q("Mehr Gehalt, oder mehr Freizeit?", ("Mehr Gehalt", "📈"), ("Mehr Freizeit", "🌴"), [47, 53]),
    q("Sportwagen, oder Eigentumswohnung?", ("Sportwagen", "🏎️"), ("Eigentumswohnung", "🏢"), [48, 52]),
    q("Sparen, oder Urlaub?", ("Sparen", "🐷"), ("Urlaub", "✈️"), [41, 59]),
  ], outro=OUTRO_POLL)

V["g10"] = dict(format="story", voice=BRIAN,
  claim={"title": "DEIN LEBEN", "sub": "DEINE WAHL", "say": "Dein Leben. Deine Wahl. Merk dir deine Antworten!", "glitch": "robot"},
  questions=[
    q("Du bist 18 und erbst 10.000 Euro. Ein Auto, oder alles in einen ETF?", ("A: Auto kaufen", "🚗"), ("B: Alles in ETF", "📈"), [58, 42]),
    q("Du bist 20. Ausbildung mit Gehalt, oder Studium ohne Gehalt?", ("A: Ausbildung", "🛠️"), ("B: Studium", "🎓"), [46, 54]),
    q("Du bist 25. Eigene Wohnung, oder WG und 500 Euro sparen?", ("A: Eigene Wohnung", "🏠"), ("B: WG + sparen", "👥"), [63, 37]),
    q("Du bist 30. Haus kaufen, oder weiter mieten und investieren?", ("A: Haus kaufen", "🏡"), ("B: Mieten + investieren", "📊"), [55, 45]),
    q("Du bist 35. Selbstständig machen, oder sicherer Job?", ("A: Selbstständig", "🚀"), ("B: Sicherer Job", "🏛️"), [41, 59]),
    q("Du bist 40. Rente mit 55, oder mit 67 und doppelt so viel?", ("A: Rente mit 55", "🏖️"), ("B: Rente mit 67, doppelt", "💶"), [66, 34]),
  ], outro={"say": "Was ist dein Weg? Schreib ihn in die Kommentare!", "title": "WAS IST DEIN WEG?",
            "sub": "z.B. A-B-B-A-B-A in die Kommentare", "share": "Schick das an jemanden und vergleicht eure Wege",
            "shareSay": "Und schick das an jemanden und vergleicht eure Wege!"})

for vid, d in V.items():
    v = {"id": vid, "channel": "G", "handle": None, "format": d["format"]}
    if d["voice"]:
        v["voice"] = d["voice"]
    if d.get("pace"):
        v["pace"] = d["pace"]
    v.update(claim=d["claim"], questions=d["questions"], outro=d["outro"])
    (OUT / f"{vid}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print(vid, d["format"], (d["voice"] or {"name": "Adam"})["name"])
