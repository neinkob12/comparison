# Deutschrap "Würdest du eher" Content Haus: Konzept (Entwurf zur Freigabe)

Status: **Wartet auf Freigabe.** Nichts davon wird gerendert, bevor Jakob die Listen abgenickt hat.

## Entscheidungen bisher

| Thema | Entscheidung |
|---|---|
| Render | Remotion (React), 1 JSON pro Video, Batch-Render zu MP4 (1080x1920, 30fps) |
| Stimme | ElevenLabs (deutsch), Key kommt als Env-Variable `ELEVENLABS_API_KEY` |
| Look | Split-Screen oben rot / unten blau, Bild + Name, Prozent ploppt auf |
| Musik | Keine eingebrannt, Trend-Sound beim Upload in TikTok |
| Upload | Erst manuell / Scheduler, später API |
| Kanäle | 2 Kanäle, gleiche Nische (New Gen), 25 Videos je Kanal, A/B-Test |
| Fokus | New Gen Deutschrap |
| Prozente | Bewusst provokant (knappe oder überraschende Ergebnisse) |
| Ton | Locker + Meme, keine Beleidigungen oder falschen Behauptungen |

## Videoaufbau (ca. 65 bis 75 Sekunden)

| Abschnitt | Dauer | Inhalt |
|---|---|---|
| Hook + Follow | 4 s | "Folg mir, wenn du bei mindestens 4 gleich gewählt hast!" + Follow-Button-Animation |
| Frage 1 bis 3 | je ca. 10 s | TTS liest Frage, 3-Sek-Countdown-Balken, Prozente ploppen auf, Gewinner pulsiert |
| Chaos-Frage (Mitte) | 9 s | Absurde Off-Topic-Frage im gleichen Layout, andere Farbe |
| Frage 4 bis 6 | je ca. 10 s | wie oben |
| Outro + Follow | 4 s | "Schreib in die Kommentare, wie oft du mit der Mehrheit warst. Folgen für Teil 2!" |

Standard: **6 Vergleiche + 1 Chaos-Frage**. Kanal A und Kanal B bekommen leicht unterschiedliche Farben und Stimmen (A/B-Test).

## Rapper-Pool (New Gen + ein paar Crossover-Namen)

**New Gen Kern:** Ski Aggu, Pashanim, Nina Chuba, Luciano, Apache 207, Makko, Symba, Badmomzjay, Zartmann, Paula Hartmann, Ayliva, Jazeek, Domiziana, Kasimir1441, Berq, 1986zig, t-low, Sira, Lune, Haiyti, Montez, Nimo

**Crossover (für Kontrast, sorgt für Kommentare):** Shirin David, Sido, Capital Bra, Cro, Yung Hurn, Ufo361, RAF Camora, Bonez MC, Haftbefehl, Shindy, Peter Fox

**Gruppen / Crews:** 187 Strassenbande, K.I.Z, BHZ, Kitschkrieg, Genetikk, SXTN (Nostalgie)

**Szenen:** Berlin, Frankfurt, Hamburg, Wien, Ruhrpott, Stuttgart

## Song-Pool (vor Rendern per Spotify verifiziert)

| Artist | Songs |
|---|---|
| Ski Aggu | Friesenjung, Party Sahne |
| Pashanim | Sommergewitter, Airwaves |
| Nina Chuba | Wildberry Lillet, Fame, Mangos mit Chili |
| Luciano | Bamba |
| Apache 207 | Roller, Komet, Fühlst du das nicht auch |
| Zartmann | Tau mich auf |
| Ayliva | Sie weiß |
| Shirin David | Bauch Beine Po, Ich darf das, Gib ihm |
| Sido | Mein Block, Bilder im Kopf, ISSA |
| Capital Bra | Cherry Lady, Berlin lebt |
| Cro | Easy, Einmal um die Welt |
| Yung Hurn | Ok cool, Bianco |
| Bonez MC & RAF Camora | Palmen aus Plastik, 500 PS |
| Haftbefehl | Chabos wissen wer der Babo ist |
| Peter Fox | Haus am See, Zukunft Pink |

Weitere Songs (Makko, Symba, Badmomzjay, Jazeek usw.) ziehe ich per Spotify-Suche nach, damit nichts falsch zugeordnet wird.

## Frageformate (Würdest du eher ...)

1. **Nur noch hören:** "... ein Jahr nur noch Ski Aggu oder nur noch Pashanim hören?"
2. **Song verbannen:** "... Friesenjung oder Wildberry Lillet für immer aus Spotify löschen?"
3. **Konzert:** "... erste Reihe bei Apache 207 oder Backstage bei Nina Chuba?"
4. **Album auf einsamer Insel:** "... nur Album X oder nur Album Y mitnehmen?"
5. **Feature:** "... ein Feature mit Luciano oder mit Shirin David bekommen?"
6. **Alltag mit Rapper:** "... mit Makko WG teilen oder mit Symba Roadtrip machen?"
7. **Crew/Gruppe:** "... Teil von 187 oder Teil von K.I.Z sein?"
8. **Szene:** "... nur noch Berlin-Rap oder nur noch Wien-Rap?"
9. **Generationen-Clash:** "... Cro 2012 live oder Ski Aggu 2026 live?"
10. **Lyrics-Fail:** "... auf der Hochzeit Mein Block oder Bauch Beine Po performen müssen?"

## Chaos-Fragen (Mitte, Pool zum Rotieren)

- Nie wieder duschen ODER nie wieder Maka
- Triff dich im Park mit der 3. Person unter "Teilen" ODER schick deinen letzten Screenshot in die Familiengruppe
- Deine Mutter liest deinen kompletten Chatverlauf ODER dein Ex sieht deinen Suchverlauf
- Ein Jahr kein Döner ODER ein Jahr kein WLAN
- Ruf die 5. Person in deinen Kontakten an und sag "Ich liebe dich" ODER poste das 1. Foto in deiner Galerie in die Story
- Für immer nasse Socken ODER für immer Sand im Schuh
- Nur noch Schlager hören ODER nur noch Crocs tragen
- Dein Lehrer/Chef sieht dein Spotify Wrapped ODER deine Screentime

## Verteilung der 50 Videos

| Format | Anzahl |
|---|---|
| Nur noch hören (Rapper vs Rapper) | 10 |
| Songs (verbannen / Hochzeit / Dauerschleife) | 9 |
| Konzerte | 8 |
| Alben | 6 |
| Feature / Alltag mit Rapper | 7 |
| Crews + Szenen | 5 |
| Generationen-Clash (New Gen vs OG) | 5 |

## Beispielskript (Video 1, Kanal A)

> Hook: "Folg mir, wenn du bei mindestens 4 gleich gewählt hast wie die Mehrheit!"
>
> 1. Ein Jahr nur Ski Aggu ODER ein Jahr nur Pashanim? (41 / 59)
> 2. Erste Reihe bei Apache 207 ODER Backstage bei Nina Chuba? (63 / 37)
> 3. Friesenjung für immer löschen ODER Sommergewitter für immer löschen? (52 / 48)
> 4. **Chaos:** Nie wieder duschen ODER nie wieder Maka? (18 / 82)
> 5. Feature mit Luciano ODER Feature mit Shirin David? (47 / 53)
> 6. Mit Makko in eine WG ODER mit Zartmann auf Tour? (35 / 65)
> 7. Cro 2012 live ODER Ski Aggu 2026 live? (71 / 29)
>
> Outro: "Wie oft warst du bei der Mehrheit? Ab in die Kommentare und folgen für Teil 2!"

## Offene Punkte / Blocker

- **Netzwerk:** `api.elevenlabs.io` und Bildquellen (z.B. `commons.wikimedia.org`, `upload.wikimedia.org`) sind in der Cloud-Umgebung gerade gesperrt. Muss in den Environment-Settings freigegeben werden.
- **ElevenLabs Key:** als Env-Variable `ELEVENLABS_API_KEY` in der Umgebung hinterlegen (nicht im Chat posten). Wird erst in einer neuen Session sichtbar.
- **Bilder:** Plan ist Wikimedia Commons (CC-lizenziert, deutlich sicherer als Spotify-Bilder). Fehlende Bilder liefert ihr nach.
- **Kanalnamen:** noch offen, Vorschläge siehe Chat.
