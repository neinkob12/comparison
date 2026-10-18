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
| Kanäle | 2 Kanäle, 25 Videos je Kanal, A/B-Test. Kanal A: https://www.tiktok.com/@akhmachtkrach19 |
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

**Kern (von Jakob gesetzt):** Nizi19, Lucio101, Lacazette, Pashanim, Yuyu19, Kalim (Symba gestrichen)

**1019 & Umfeld:** Omar101, Karamel19 (beide 1019), Makko, Mucco (oft mit Lacazette), Caney030 (auf Akh & Krach)

**Berliner Trap:** Ufo361 (Hier mit Lucio101), Luciano (Feature mit Kalim), Samra, Souly, Zackavelli (Beyazz von Jakob gestrichen)

Fotos werden über die Upload-Seite gesammelt: https://claude.ai/artifact/TtAw226hCZAuFdRQFgSY3d

## Song- und Album-Pool (recherchiert)

| Artist | Songs | Alben |
|---|---|---|
| Lacazette | LID, CUP, FTW, H&K, +49 (mit Lucio101, Nizi19, Yuyu19) | LID |
| Lucio101 | Superkraft, Wittenbergplatz, Hier (mit Ufo361), 6 Nullen, Schuhkarton | 101%, Mittendrin, 1019 (mit Nizi19) |
| Nizi19 | Hollywoodreif, Million (1019) | Doktor, Akh & Krach (mit Yuyu19) |
| Yuyu19 | Hollywoodreif, Hajar, Schoko und Keks, Schein trügt | Akh & Krach |
| Pashanim | Sommergewitter, Airwaves, Kleiner Prinz, Bagchaser Can, Ms. Jackson, Hauseingang | |
| Kalim | 16, SKRR, bis um 3, Bleib über Nacht (feat. Luciano) | Free Game, Nur für meine Augen |

## Formate

| Format | Beispiel |
|---|---|
| Rapper vs Rapper | Ein Jahr nur Lacazette oder ein Jahr nur Pashanim? |
| Song vs Song | CUP oder Sommergewitter für immer löschen? |
| Konzert | Lucio101 erste Reihe oder Kalim backstage? |
| Album | Nur noch LID oder nur noch 101%? |
| Feature | Feature mit Nizi19 oder mit Kalim? |

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
> 3. Feature mit Nizi19 oder mit Kalim? (73 / 27)
> 4. **Zwischenfrage:** Nie wieder duschen oder nie wieder Maka? (18 / 82)
> 5. Nur noch LID oder nur noch 101%? (49 / 51)
> 6. Lucio101 erste Reihe oder Kalim backstage? (44 / 56)
>
> Outro: "Wie oft lagst du bei der Mehrheit? Schreibs in die Kommentare und folg für Teil 2."

## Bilder

Von Spotify geholt (offizielle Artist-Bilder und Cover), liegen lokal unter `assets/` (nicht im Git, Rechte liegen bei Spotify/Labels) und auf der Upload-Seite.

Fehlen noch:
- Nichts. Pashanim-Cover kommen von Apple Music, Ufo361 ist aus dem Cover von "Emotions 2.0" ausgeschnitten.

Fehlt ein Bild, rendert das Template eine Namens-Karte (großer Name auf Farbe).

## Sprache / Formulierung

- Kurz und direkt: "Ein Tag mit Pashanim oder ein Tag mit Lucio101?" Keine Füllwörter wie "abhängen".
- Kein gesprochener Countdown vor der Auflösung.
- Aussprache aller Namen steht in `config/aussprache.json` und wird vor jedem TTS-Aufruf ersetzt.
- Zahlen in Namen immer als einzelne Ziffern: Nizi19 = "Nizi Eins Neun", Lucio101 = "Lussio Eins Null Eins".
- LID und FTW buchstabiert, CUP als Wort.
- Aussprache wird als Lautschrift im Text übergeben. Echte Lautschrift-Tags (IPA) unterstützt ElevenLabs nur bei den englischen Modellen, nicht bei Adam auf Deutsch.
- Gegen komische Atempausen: jede Zeile einzeln vertonen, Stabilität 0.7, keine "..." und keine Kommas in Namen, Stille am Anfang/Ende automatisch abschneiden, lange Pausen im Satz auf max. 0.3 s kürzen.

## Kanäle und A/B-Test (Hook)

Beide Kanäle bekommen die gleichen Fragen, nur der Einstieg unterscheidet sich.

| | Kanal A: "Hart rein" | Kanal B: "Rapper-Duell" |
|---|---|---|
| Sekunde 0 | Sofort eine provokante Frage als Riesentext + Stimme, z.B. "Eine Nacht mit Nizi19 oder nie wieder Lucio101 hören?" | Titelkarte "RAPPER-DUELL" + Stimme: "Rapper-Duell. Heute: 1019 gegen den Rest." (2 bis 3 Sekunden) |
| Danach | Auflösung dieser Frage, dann normal weiter | Erste Frage |
| Follow-Aufruf | Nach Frage 1 kurz eingeblendet | Direkt nach der Titelkarte |

Messung nach 7 Tagen: durchschnittliche Wiedergabezeit, Anteil nach 3 Sekunden noch dabei, Kommentare pro 1000 Views, neue Follower.

## Update: nur Kanal A

Kanal B ("Rapper-Duell") ist vorerst gestrichen. Wir machen nur Kanal A (@akhmachtkrach19, hart rein mit Hook-Frage).
Lucio101 heißt in Kanal A nur "Lucio". Nizi19 bleibt mit 19. Yuyu19 heißt in jedem Video "Haribo".
Ende: "Wie oft lagst du richtig, Akh? Schreibs in die Kommentare!"
Countdown: heller Uhr-Tick, 5 pro Sekunde, nachgebaut nach Jakobs Referenzvideo.

## Update 16.10.: Hook nach a01 (15k Views)

a01 ging durch, a02-a04 nicht. Einziger Unterschied war die Hook-Frage. Ab a05 daher die a01-Formel: **"Eine Nacht mit X, oder nie wieder Y hören?"**, extreme Prozente (unter 12 / über 88), große Namen bei "nie wieder".

- Hook ab Frame 0 komplett sichtbar (beide Bilder, kein Reinfliegen), gelber Sticker "WAS WÄHLT DIE MEHRHEIT? 👀", Einschlag + Ring + Pop als Sound, Stimme 1.12x.
- Hook-Timer zeigt 3-2-1, läuft aber in 1.5 s ab (Tick doppelt so schnell). Alle anderen Timer 2.7 s. Stimme sonst 1.05x.
- Follow-Popup mittig, Rest unscharf, ca. 0.7 s.
- Upload: siehe `docs/upload_checkliste.md` (KI-Label, Cover, Sound Solitude, alle Rapper als Hashtags).
