# Plan: Eigene TikTok-API-App einreichen

Ziel: eine kleine, **öffentliche** Web-App (Video-Scheduler für Creator), die TikToks App-Review besteht, damit Videos offiziell per Content Posting API gepostet werden können.

## Die wichtigste Regel

TikTok lehnt Apps ab, die nur für dich sind:
> "Apps must not be for private or personal use."
> "Apps must not be limited to test use or to internal or private team accounts."
> "Apps that are still in development or testing will not be approved."

Heißt: Es muss ein **echtes, fertiges Produkt** sein, das andere Creator auch nutzen können (z.B. kostenlos). Nicht nur so tun, wirklich so bauen.

## Was wir brauchen

### Accounts und Kosten
| Was | Kosten | Wer |
|---|---|---|
| TikTok-Developer-Account (developers.tiktok.com) | 0 € | Jakob |
| Domain (z.B. `kurzplan.app`, `slotpost.app`, `reelslot.app`, `cliptakt.de`, alle frei am 19.10.) | ca. 10 bis 20 €/Jahr | Jakob kauft |
| Hosting Vercel | 0 € (Hobby) | schon verbunden |
| Datenbank + Video-Speicher Supabase | 0 € (Free) | schon verbunden |
| Kontakt-Mail mit der Domain (für Impressum/Datenschutz) | 0 € (Weiterleitung) | Jakob |

### App-Daten fürs Formular
- **Name:** eigener Name, **kein "TikTok"** drin, muss zur Website passen
- **Icon:** 1024 x 1024 px, PNG/JPG, max. 5 MB, darf keiner bekannten Marke ähneln
- **Kategorie** und **Beschreibung** (sehen Nutzer beim Login)
- **Website-URL:** echte Seite, **keine** reine Landing- oder Login-Seite
- **Terms of Service** und **Privacy Policy:** eigene Seiten, Links **direkt sichtbar** (Footer, nicht im Menü)
- **Redirect URI** für "Login mit TikTok" (z.B. `https://DOMAIN/api/auth/tiktok/callback`)
- **URL-Verifizierung:** Domain per DNS-Eintrag oder Datei bestätigen (Website, Terms, Privacy, Video-URL)

### Produkte und Berechtigungen (Scopes)
| Produkt / Scope | Wofür | Begründung im Formular |
|---|---|---|
| Login Kit, `user.info.basic` | Nutzer verbindet sein Konto, wir zeigen Name/Bild | Nutzer sieht, auf welches Konto gepostet wird |
| Content Posting API, `video.publish` (Direct Post) | geplante Videos zur gewählten Zeit veröffentlichen | Kernfunktion: Scheduling |
| Content Posting API, `video.upload` | Video als Entwurf in die TikTok-App schicken | für Creator, die vor dem Posten noch Sound/Effekte in der App hinzufügen wollen |

Nur anfragen, was die App wirklich nutzt und was im Demo-Video zu sehen ist.

### Pflicht-Oberfläche beim Posten (TikTok UX-Regeln)
- Creator-Info bei jedem Öffnen frisch laden, **Nickname des Kontos anzeigen**
- Kann das Konto gerade nicht posten: abbrechen und Hinweis zeigen
- Videolänge gegen `max_video_post_duration_sec` prüfen
- Titel/Beschreibung editierbar (auch Hashtags)
- **Privatsphäre als Dropdown, ohne Vorauswahl**, Optionen exakt aus `privacy_level_options`
- Kommentare / Duett / Stitch als Häkchen, **keins vorausgewählt**, ausgegraut wenn im Konto deaktiviert
- **Werbe-Kennzeichnung:** Schalter (aus), dann "Your brand" / "Branded content" mit den exakten TikTok-Texten; Branded content nicht privat
- **KI-Kennzeichnung** (AIGC) als Option
- **Vorschau** des Videos
- Erklärung vor dem Button: Zustimmung zur **Music Usage Confirmation** (bzw. Branded Content Policy)
- Upload erst nach ausdrücklicher Zustimmung (Klick)
- Hinweis "kann ein paar Minuten dauern" + **Status anzeigen** (Status-API abfragen)
- Keine Wasserzeichen/Logos/Links ins Video einbauen

### Demo-Video (1 bis 5 Videos, je max. 50 MB)
- Kompletter Ablauf von Anfang bis Ende, im **Sandbox-Modus**
- Domain in der Adresszeile = eingetragene Website
- Zeigen: Website mit Terms/Privacy, Login mit TikTok, Consent-Seite, Upload, alle Pflicht-Felder, Absenden, Status, fertiger Post im TikTok-Konto (privat, da Sandbox)
- Jedes beantragte Produkt und jeder Scope muss vorkommen

### Was danach realistisch passiert
- Prüfung: keine offizielle Dauer, Erfahrungswerte 1 bis 3 Wochen, oft erst nach einer Ablehnung mit Feedback
- Bis zur Freigabe: alles nur privat, max. 5 Nutzer pro 24 h, Konto beim Posten privat
- Nach Freigabe: öffentlich posten, Limit ca. 15 Posts pro Creator und Tag
- **TikTok-Sounds gehen auch dann nicht per API.** Dafür gibt es den Entwurf-Weg (`video.upload`).

## Plan für morgen

| Block | Dauer | Wer | Aufgabe |
|---|---|---|---|
| 1 | 15 min | Jakob | Name entscheiden, Domain kaufen (Vercel oder Registrar), Kontakt-Mail einrichten |
| 2 | 15 min | Jakob | TikTok-Developer-Account anlegen, App erstellen (nur Name/Icon/Beschreibung), Client Key + Secret als Umgebungsvariablen in Vercel eintragen (nie in den Chat) |
| 3 | 2 bis 3 h | Claude | Web-App bauen: Website (Features, So funktioniert's, FAQ), Terms, Privacy, Impressum, Login mit TikTok, Upload-Seite nach allen UX-Regeln, Planung mit Zeitauswahl, Status-Anzeige, Supabase (Nutzer, Posts, Speicher), Cron für geplante Posts |
| 4 | 20 min | Jakob + Claude | Deploy auf Vercel, Domain verbinden, URL-Verifizierung bei TikTok |
| 5 | 20 min | Jakob | Portal: Produkte + Scopes, Redirect URI, Sandbox anlegen, eigenes TikTok-Konto als Target User |
| 6 | 30 min | Jakob | Testlauf in der Sandbox (Konto privat stellen!), Fehler an Claude |
| 7 | 20 min | Jakob | Demo-Video aufnehmen (Mac: Cmd + Shift + 5), Ablauf nach Checkliste oben |
| 8 | 15 min | Claude + Jakob | Scope-Begründungen und Beschreibung einfügen (Claude schreibt vor), einreichen |

Gesamt für Jakob: ca. 2,5 h, verteilt über den Tag.

## Vorher klären
1. Name + Domain (Vorschläge oben)
2. Eigene Mail für den Developer-Account
3. Impressum: in Deutschland für öffentliche Websites Pflicht (Name + Adresse). Eigene Adresse oder ein Impressum-Service?
