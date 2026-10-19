# Geld-Kanal: Testlauf (g01 bis g06)

Gleiches Template wie Kanal A, neue Nische mit höherem RPM.
Skripte: `scripts/generate_geld.py`, danach `python3 scripts/build.py g01 ...` und `node scripts/render.mjs g01 ...`.

## Was ist neu

| Thema | Umsetzung |
|---|---|
| Claim am Anfang | Einblendung + TTS, z.B. "80% ANTWORTEN FALSCH" (`claim` im JSON) |
| Belehrend (g01 bis g03) | Nach den Prozenten kommt eine AUFLÖSUNG: Fakt zu A, Fakt zu B, dann Stempel "BESSER" (`explain` pro Frage). Die Mehrheit liegt bewusst falsch, passt zum Claim |
| Umfrage (g04 bis g06) | Wie Kanal A, nur Prozente, 7 Fragen + Zwischenfrage |
| Hinweis | In jeder Auflösung unten klein: "Vereinfacht gerechnet. Keine Anlageberatung." |
| Bilder | Nur Emojis, keine Fotos nötig |

## Stimmen-Test

| Stimme | Videos | Einstellung |
|---|---|---|
| Adam (wie Kanal A) | g01, g04, g05 | schnell (1.18) |
| Brian (ernster, tiefer) | g02, g03, g06 | langsamer (1.06), stabiler |

Jedes Format hat beide Stimmen. Vergleichen: durchschnittliche Wiedergabezeit und Anteil "komplett angesehen" in TikTok Studio.

## Längen

| Video | Format | Stimme | Länge |
|---|---|---|---|
| g01 | belehrend | Adam | 85 s |
| g02 | belehrend | Brian | 91 s |
| g03 | belehrend | Brian | 82 s |
| g04 | Umfrage | Adam | 72 s |
| g05 | Umfrage | Adam | 72 s |
| g06 | Umfrage | Brian | 79 s |

## Gekürzt auf max. 65 s (ohne Neu-Rendern)

`python3 scripts/cut_geld.py g01 ...` schreibt `out/cut/gNN.mp4`. Bei g01 und g03 wird nur das Intro neu gerendert ("beide" statt "alle drei").

| Video | Raus | Länge |
|---|---|---|
| g01 | Ab 20 vs. ab 40 (inkl. Auflösung) | 61,2 s |
| g02 | Leasing vs. bar (inkl. Auflösung) | 65,0 s |
| g03 | Dispo vs. ETF (inkl. Auflösung) | 61,0 s |
| g04 | Gehalt vs. Kontostand öffentlich | 64,1 s |
| g05 | Chef vs. Angestellter | 63,9 s |
| g06 | Reich und einsam, Online-Shopping | 62,9 s |

## Rechnungen (geprüft)

- 1 Cent, 30 Tage verdoppelt: 0,01 × 2^29 = 5.368.709 € (Tag 20: 5.243 €)
- 100 €/Monat ab 20 bis 65 bei 7 %: ca. 379.000 € (eingezahlt 54.000 €)
- 300 €/Monat ab 40 bis 65 bei 7 %: ca. 243.000 € (eingezahlt 90.000 €)
- 10 €/Woche, 40 Jahre, 7 %: ca. 114.000 €
- 15.000 € × 1,07^10 = 29.507 €
- Leasing 299 € × 36 = 10.764 €
- 60.000 €/Jahr für immer ist bei 7 % heute ca. 857.000 € wert, also weniger als 1 Mio.
- Lotto 6 aus 49 Jackpot: 1 zu 139.838.160

## Captions

**g01:** 1 Million sofort oder 5.000 € im Monat für immer? 💰 Nur 15 % liegen bei beiden richtig 👇 #geld #finanzen #sparen #etf #würdestdueher #fyp

**g02:** Neuwagen oder Gebrauchter + investieren? 🚗 80 % antworten falsch. Du auch? 👇 #geld #finanzen #auto #leasing #würdestdueher #fyp

**g03:** Steuererklärung oder Netflix? 🧾 Nur 1 von 10 schafft beide 👇 #geld #finanzen #steuern #gehalt #würdestdueher #fyp

**g04:** 4-Tage-Woche mit 80 % Gehalt oder 5 Tage voll? 🗓️ Was hättest du gewählt? 👇 #geld #gehalt #arbeit #würdestdueher #fyp

**g05:** 500.000 € sofort oder 1 €, der sich 20 Tage verdoppelt? 🪙 Was hättest du gewählt? 👇 #geld #finanzen #million #würdestdueher #fyp

**g06:** Mit 30 in Rente mit 2.000 € oder mit 67 mit 6.000 €? 🏖️ Was hättest du gewählt? 👇 #geld #rente #finanzen #würdestdueher #fyp

## Experimente g07 bis g10

Jedes Video startet mit einem TTS-Bug (Stimme + Bild-Glitch, `glitch` im Claim). Alle direkt auf 61 bis 65 s gebaut, kein Schnitt nötig.

| Video | Format | Bug | Stimme | Länge |
|---|---|---|---|---|
| g07 | Mathe-Fallen (Auflösung) | Stotter-Loop | Adam | 63,4 s |
| g08 | Mythos oder Fakt (Aussage-Karte, RICHTIG/FALSCH) | Zeitlupe | Brian | 61,5 s |
| g09 | Speedrun, 11 Fragen, 2-Sekunden-Timer | Chipmunk | Adam | 64,4 s |
| g10 | Wähle dein Leben (Story, A/B-Kette) | Roboter | Brian | 64,9 s |

Geprüft: 0,8 × 0,8 = 0,64 (2 × 20 % = 36 %), 100 → 150 → 75 (−25 %), 3 für 2 = 33,3 %,
10.000 € / 1,02^10 ≈ 8.200 €, Trinkgeld an Angestellte steuerfrei (§ 3 Nr. 51 EStG).

## g11 bis g15: schneller Einstieg, provokante Fragen

Ausgewählt aus 16 Empfehlungen:
- **Einstieg:** Frage 1 ab Frame 0, beide Optionen sofort sichtbar. Kein Claim, kein Thema, kein Follow-Pop-up.
- **Fragen:** Geld gegen Menschen, Geld gegen Moral, brutale Tauschgeschäfte. 8 Fragen, keine Zwischenfrage.
- **Bis zum Ende halten:** Balken "FRAGE 3/8" oben, Pop-up "Die letzte Frage spaltet alle 👀" nach Frage 4, 2-Sekunden-Timer, Loop-Ende ("Und jetzt mal ehrlich:" führt zurück in Frage 1).
- **Kommentare:** extreme Prozente (3/97, 50/50), Pop-up "Markier jemanden, der … nimmt 👇" nach Frage 3.

Optionen im JSON: `instant`, `progress`, `follow: false`, `popup` pro Frage, `outro.loop`.

| Video | Schwerpunkt | Stimme | Länge |
|---|---|---|---|
| g11 | Geld gegen Freunde/Partner | Adam | 61,1 s |
| g12 | Geld gegen Moral | Adam | 61,5 s |
| g13 | Brutale Tauschgeschäfte | Adam | 62,9 s |
| g14 | Geld in Beziehungen | Brian | 62,8 s |
| g15 | Mix | Adam | 63,8 s |
