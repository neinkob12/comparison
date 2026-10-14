# Deutschrap "Würdest du eher" Content Haus: Konzept (Entwurf v2 zur Freigabe)

Status: **Wartet auf Freigabe.** Nichts wird gerendert, bevor Jakob die Listen abgenickt hat.

## Entscheidungen bisher

| Thema | Entscheidung |
|---|---|
| Render | Remotion (React), 1 JSON pro Video, Batch-Render zu MP4 (1080x1920, 30fps) |
| Stimme | ElevenLabs "Adam" (pNInz6obpgDQGcFmaJgB), Modell eleven_multilingual_v2, Key als `ELEVENLABS_API_KEY` |
| Look | Split-Screen oben rot / unten blau, Bild + Name, Prozent ploppt auf |
| Musik | Keine eingebrannt, Trend-Sound beim Upload in TikTok |
| Upload | Erst manuell / Scheduler, später API |
| Kanäle | 2 Kanäle, gleiche Nische, 25 Videos je Kanal, A/B-Test |
| Fokus | **Nur New School**, Berliner 1019-Umfeld + nahe Artists. Keine Old School, kein Generationen-Vergleich |
| Prozente | Bewusst provokant (knappe oder überraschende Ergebnisse) |
| Ton | Locker, keine Beleidigungen oder falschen Behauptungen |

## Videoaufbau (ca. 65 bis 75 Sekunden)

| Abschnitt | Dauer | Inhalt |
|---|---|---|
| Intro + Follow | 4 s | "Folg für Teil 2" + Follow-Button-Animation |
| Frage 1 bis 3 | je ca. 10 s | TTS liest Frage, kurze Pause (kein gesprochener Countdown), Prozente ploppen auf |
| Zwischenfrage | 9 s | Off-Topic-Frage ("Nie wieder duschen oder nie wieder Maka") |
| Frage 4 bis 6 | je ca. 10 s | wie oben |
| Outro + Follow | 4 s | Kommentar-Aufruf + Follow |

## Rapper-Pool

**Kern (von Jakob gesetzt):** Nizi19, Lucio101, Lacazette, Pashanim, Symba, Yuyu19, Kalim

**1019 & Umfeld:** Omar101, Karamel19 (beide 1019), Makko (Feature mit Symba), Mucco (oft mit Lacazette), Caney030 (auf Akh & Krach), Pajel (16 mit Kalim)

**Berliner Trap:** Ufo361 (Hier mit Lucio101), Luciano (Feature mit Kalim), Jazeek, Samra, Souly, Zackavelli (Beyazz von Jakob gestrichen)

Fotos werden über die Upload-Seite gesammelt: https://claude.ai/artifact/TtAw226hCZAuFdRQFgSY3d

## Song- und Album-Pool (recherchiert)

| Artist | Songs | Alben |
|---|---|---|
| Lacazette | LID, CUP, FTW, H&K, +49 (mit Lucio101, Nizi19, Yuyu19) | LID |
| Lucio101 | Superkraft, Wittenbergplatz, Hier (mit Ufo361), 6 Nullen, Schuhkarton | 101%, Mittendrin, 1019 (mit Nizi19) |
| Nizi19 | Feuermelder (mit Lucio101), Hollywoodreif, Million (1019) | Doktor, Akh & Krach (mit Yuyu19) |
| Yuyu19 | Hollywoodreif, Hajar, Schoko und Keks, Schein trügt | Akh & Krach |
| Pashanim | Sommergewitter, Airwaves, Kleiner Prinz, Bagchaser Can, Ms. Jackson, Hauseingang | |
| Symba | Angels Sippen, Mario Run, Memos (feat. Makko) | Teamboys undso |
| Kalim | 16 (mit Pajel), SKRR, bis um 3, Bleib über Nacht (feat. Luciano) | Free Game, Nur für meine Augen |

## Formate

| Format | Beispiel |
|---|---|
| Rapper vs Rapper | Ein Jahr nur Lacazette oder ein Jahr nur Pashanim? |
| Song vs Song | CUP oder Sommergewitter für immer löschen? |
| Konzert | Lucio101 erste Reihe oder Kalim backstage? |
| Album | Nur noch LID oder nur noch 101%? |
| Feature | Feature mit Nizi19 oder mit Symba? |

## Zwischenfragen (Pool zum Rotieren)

- Nie wieder duschen oder nie wieder Maka
- Im Park mit der 3. Person unter "Teilen" treffen oder deinen letzten Screenshot in die Familiengruppe schicken
- Deine Mutter liest deine Chats oder dein Ex sieht deinen Suchverlauf
- Ein Jahr kein Döner oder ein Jahr kein WLAN
- Die 5. Person in deinen Kontakten anrufen und "Ich liebe dich" sagen oder das 1. Foto in deiner Galerie in die Story posten
- Für immer nasse Socken oder für immer Sand im Schuh
- Dein Chef sieht dein Spotify Wrapped oder deine Bildschirmzeit

## Verteilung der 50 Videos

| Format | Anzahl |
|---|---|
| Rapper vs Rapper | 14 |
| Song vs Song | 13 |
| Konzert | 8 |
| Album | 7 |
| Feature | 8 |

Meist gemischt pro Video (6 Fragen aus 2 bis 3 Formaten), damit es nicht eintönig wird.

## Beispielskript (Video 1, Kanal A)

> Intro: "Folg für Teil 2, wir fangen direkt an."
>
> 1. Ein Jahr nur Lacazette oder ein Jahr nur Pashanim? (54 / 46)
> 2. CUP oder Sommergewitter für immer löschen? (61 / 39)
> 3. Feature mit Nizi19 oder mit Symba? (73 / 27)
> 4. **Zwischenfrage:** Nie wieder duschen oder nie wieder Maka? (18 / 82)
> 5. Nur noch LID oder nur noch 101%? (49 / 51)
> 6. Lucio101 erste Reihe oder Kalim backstage? (44 / 56)
>
> Outro: "Wie oft lagst du bei der Mehrheit? Schreibs in die Kommentare und folg für Teil 2."

## Bilder

Von Spotify geholt (offizielle Artist-Bilder und Cover), liegen lokal unter `assets/` (nicht im Git, Rechte liegen bei Spotify/Labels) und auf der Upload-Seite.

Fehlen noch:
- **Symba:** Spotify hat für ihn kein Artist-Bild (der Treffer war ein anderer Symba)
- **Pashanim-Songs** (Sommergewitter, Airwaves, Kleiner Prinz): seine Musik ist auf Spotify gerade gesperrt, nur sein Profilbild ist noch da
- **Feuermelder:** nicht gefunden
- **Ufo361:** sein Spotify-Bild ist eine Lego-Ninja-Figur, besser austauschen

Fehlt ein Bild, rendert das Template eine Namens-Karte (großer Name auf Farbe).

## Sprache / Formulierung

- Kurz und direkt: "Ein Tag mit Pashanim oder ein Tag mit Lucio101?" Keine Füllwörter wie "abhängen".
- Kein gesprochener Countdown vor der Auflösung.
- Aussprache aller Namen steht in `config/aussprache.json` und wird vor jedem TTS-Aufruf ersetzt.
- Zahlen in Namen immer als einzelne Ziffern: Nizi19 = "Nizi Eins Neun", Lucio101 = "Lussio Eins Null Eins".
- LID und FTW buchstabiert, CUP als Wort.

## Kanäle und A/B-Test (Hook)

Beide Kanäle bekommen die gleichen Fragen, nur der Einstieg unterscheidet sich.

| | Kanal A: "Hart rein" | Kanal B: "Rapper-Duell" |
|---|---|---|
| Sekunde 0 | Sofort eine provokante Frage als Riesentext + Stimme, z.B. "Eine Nacht mit Nizi19 oder nie wieder Lucio101 hören?" | Titelkarte "RAPPER-DUELL" + Stimme: "Rapper-Duell. Heute: 1019 gegen den Rest." (2 bis 3 Sekunden) |
| Danach | Auflösung dieser Frage, dann normal weiter | Erste Frage |
| Follow-Aufruf | Nach Frage 1 kurz eingeblendet | Direkt nach der Titelkarte |

Messung nach 7 Tagen: durchschnittliche Wiedergabezeit, Anteil nach 3 Sekunden noch dabei, Kommentare pro 1000 Views, neue Follower.
