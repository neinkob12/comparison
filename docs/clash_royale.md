# Clash Royale Vergleichsvideos: Assets und Mockups

## Was da ist (`assets/clash_royale/`)

| Ordner | Inhalt |
|---|---|
| `cards/` | 208 Kartenbilder 302x363: alle Basiskarten, 49 Evolutionen (`*-ev1`), Helden (`*-hero`) |
| `cards.csv` | 204 Karten mit Name en/de, Elixier, Seltenheit, Typ, Variante. 10 Event-/Altkarten ohne Werte |
| `arenas/` | 37 Arena-Renders und Liga-Abzeichen (512x512) |
| `chests/`, `tokens/`, `ui/` | Truhen, Tausch-Tokens, blaues Menue-Rautenmuster, XP-Stern |
| `champions/` | 4 grosse Champion-Renders (Golden Knight, Archer Queen, Mighty Miner, Skeleton King) |
| `chr/` | 166 grosse Figuren-Renders, nicht im Repo: `python3 scripts/fetch_cr_assets.py --chr` |
| `sfx/`, `music/` | Countdown 1-10, Kronen, Karten-Sounds, Kampfmusik-Loop, Menue-Musik |
| `backdrops/` | 1080x1920 Hintergruende: Arena-Split (rot oben, blau unten), Menue-Blau, Lila-Strahlen, Gold-Strahlen, 6 weichgezeichnete Arenen |
| `fonts/` | Lilita One (nah an der CR-Schrift, frei) |

Neu holen oder aktualisieren: `python3 scripts/fetch_cr_assets.py` und `python3 scripts/cr_backdrops.py`.
Lizenz und Pflicht-Hinweis: `assets/clash_royale/LIZENZ.md`.

## Mockups (`content/clash_royale/mockups/`)

HTML pro Layout, gerendert nach `png/` mit `sh content/clash_royale/mockups/render.sh`.

1. **Card vs Card**: Arena-Split wie im Spiel, Gegner oben rot, du unten blau, VS auf dem Fluss, Prozente. Passt 1:1 zum bestehenden Comparison-Look.
2. **Evo vs Hero**: "Would you rather", Lila-Strahlen, Balken-Umfrage.
3. **Elixier-Quiz**: Menue-Blau, Timer, 4 Antwort-Buttons. Passt zum Quiz-Format (Quiz.tsx).
4. **Tier-Liste**: S bis D mit Kartenbildern, Teaser fuer den naechsten Teil.
5. **Champion 1v1**: Gold-Strahlen, grosse Renders, Kronen-HUD mit Timer, Truhe.

Prozente und Tier-Einordnungen in den Mockups sind Platzhalter.

## Naechste Schritte

- Sprache und Kanal festlegen (eigener CR-Kanal, Englisch oder Deutsch; `cards.csv` hat beide Namen).
- Lieblings-Layouts auswaehlen, dann als Remotion-Komposition bauen (Comparison.tsx um `theme: "cr"` erweitern statt neu schreiben).
- TikTok-Sicherheitszone beachten: unten ca. 300 px und rechts ca. 150 px frei lassen.
- Fragen-Listen schreiben (Karte vs Karte, Evo vs Held, Elixier-Quiz) und Elixierwerte gegen das aktuelle Spiel pruefen.
- Pflicht-Hinweis in jede CR-Caption.
