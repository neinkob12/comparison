# Deutschrap "Würdest du eher" Content Haus: Konzept (Entwurf v2 zur Freigabe)

Status: **Wartet auf Freigabe.** Nichts wird gerendert, bevor Jakob die Listen abgenickt hat.

## Entscheidungen bisher

| Thema | Entscheidung |
|---|---|
| Render | Remotion (React), 1 JSON pro Video, Batch-Render zu MP4 (1080x1920, 30fps) |
| Stimme | ElevenLabs (deutsch), Key liegt als `ELEVENLABS_API_KEY` in der Umgebung |
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
| Frage 1 bis 3 | je ca. 10 s | TTS liest Frage, 3-Sek-Countdown, Prozente ploppen auf |
| Zwischenfrage | 9 s | Off-Topic-Frage ("Nie wieder duschen oder nie wieder Maka") |
| Frage 4 bis 6 | je ca. 10 s | wie oben |
| Outro + Follow | 4 s | Kommentar-Aufruf + Follow |

## Rapper-Pool

**Kern (von Jakob gesetzt):** Nizi19, Lucio101, Lacazette, Pashanim, Symba, Yuyu19, Kalim

**Nah dran (gleiche Crew / häufige Features):** Omar101, Karamel19 (beide 1019), Makko (Feature mit Symba), Mucco (oft mit Lacazette), Caney030 (auf Akh & Krach), Luciano (Feature mit Kalim), Pajel (16 mit Kalim), Ufo361 (Hier mit Lucio101)

**Newcomer (optional, kleinere Reichweite):** Soyhan (Wedding), Gangsta Ralph

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
| Crew | Einen Tag mit 1019 abhängen oder einen Tag mit Lacazette? |

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
| Rapper vs Rapper | 12 |
| Song vs Song | 12 |
| Konzert | 8 |
| Album | 7 |
| Feature | 6 |
| Crew | 5 |

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
> 7. Einen Tag mit 1019 oder einen Tag mit Lacazette? (66 / 34)
>
> Outro: "Wie oft lagst du bei der Mehrheit? Schreibs in die Kommentare und folg für Teil 2."

## Bilder

Wikimedia Commons hat für diese Szene fast nichts (Stand Check heute): kein Foto von Pashanim, Yuyu19, Karamel19; bei Lacazette nur der Fußballer; Lucio101 und Makko je ein Foto. **Bilder müssen von euch kommen.**

Ablage: `assets/artists/<slug>.jpg` (Hochformat oder quadratisch, mind. 800 px), z.B. `lacazette.jpg`, `lucio101.jpg`, `nizi19.jpg`, `yuyu19.jpg`, `pashanim.jpg`, `symba.jpg`, `kalim.jpg`. Album-Cover analog unter `assets/albums/<slug>.jpg`.

Fehlt ein Bild, rendert das Template automatisch eine Namens-Karte (großer Name auf Farbverlauf), damit nichts blockiert.
