# Setup für das Team

Alles, was du brauchst, um Videos zu erzeugen und auf TikTok einzuplanen. Mac, einmalig ca. 20 Minuten.

## 1. Zugang

1. GitHub-Einladung zum Repo `neinkob12/comparison` annehmen (Mail von GitHub).
2. Den ElevenLabs-Key bekommst du **privat** von Jakob (nie in den Chat einer Gruppe, nie ins Repo).

## 2. Werkzeuge installieren (Terminal)

Homebrew, falls `brew --version` "command not found" sagt:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Danach die "Next steps" ausführen, die es am Ende anzeigt.

```
brew install git gh node ffmpeg
brew install --cask miniconda
conda init zsh
```
Terminal schließen und neu öffnen.

## 3. Repo holen

```
gh auth login
cd ~
gh repo clone neinkob12/comparison
cd comparison
```
Bei `gh auth login` überall Enter drücken, im Browser einloggen.

## 4. Upload-Tool einrichten

```
conda create -y -n tiktok python=3.12
conda activate tiktok
python -m pip install tiktokautouploader
phantomwright_driver install chromium
cd "$(python -c "import tiktokautouploader, os; print(os.path.dirname(tiktokautouploader.__file__))")/Js_assets"
npm install
cd ~/comparison
```

## 5. TikTok-Konto einloggen (einmal pro Konto)

**Wichtig:** Der QR-Code loggt das Konto ein, das **gerade in der TikTok-App auf deinem Handy offen ist**. Vorher in der App auf das richtige Konto wechseln.

```
conda activate tiktok
cd "$(python -c "import tiktokautouploader, os; print(os.path.dirname(tiktokautouploader.__file__))")/Js_assets"
node login.js
```
Einloggen. Das Fenster schließt sich, sobald du auf der For-You-Seite bist (sonst `tiktok.com/foryou` eintippen). Dann, mit dem Kontonamen aus `config/accounts.json`:
```
mv TK_cookies.json ~/comparison/TK_cookies_KONTO.json
cd ~/comparison
```
Die Datei `TK_cookies_KONTO.json` ist wie ein Passwort: nie teilen, sie ist in `.gitignore`.

## 6. Jeden Tag / jede Session

```
cd ~/comparison
conda activate tiktok
git pull
```

## 7. Hochladen

```
python scripts/tiktok_upload.py status                          # Wer hat was eingeplant, wie viele Tage sind abgedeckt
python scripts/tiktok_upload.py test a17 --account KONTO        # 1 Video als Entwurf (zum Prüfen)
python scripts/tiktok_upload.py plan a17 a50 --account KONTO    # einplanen laut Plan, max. 10 Tage voraus
python scripts/tiktok_upload.py mark a01 a16 --account KONTO    # von Hand gepostete Videos als erledigt eintragen
```

Pro Video macht das Script: Video, Beschreibung, Hashtags, Sound aus den Favoriten (Lautstärke + Fade-in), Cover, KI-Kennzeichnung, Uhrzeit. Klappt ein Schritt nicht automatisch, hält es an und sagt, was du im Browser von Hand machen sollst, dann Enter.

Die Videos müssen in `out/cut/` liegen (z.B. `out/cut/a17.mp4`). Cover: `out/cover/a17.jpg`, sonst wird eins aus Sekunde `cover_at` geschnitten.

**Tracking:** Jeder Upload landet in `docs/upload_log.csv` und wird automatisch nach GitHub gepusht. Schon eingeplante Videos überspringt das Script (auch wenn ein anderer sie eingeplant hat), deshalb vorher immer `git pull`. Den Sound vorher in der TikTok-App für das Konto **favorisieren**.

## 8. Neues Konto anlegen

In `config/accounts.json` einen Eintrag ergänzen:
```json
"neues_konto": {
  "kanal": "B",
  "betreut_von": "Name",
  "plan": "docs/plan_neues_konto.csv",
  "sound": "Stichwort aus dem Favoriten-Sound",
  "music_db": -12,
  "fade_in": 2.5,
  "cover_at": 5
}
```
Plan-Datei im gleichen Format wie `docs/posting_plan.csv` (`datum,uhrzeit,datei,caption`). Dann Login (Schritt 5) mit `TK_cookies_neues_konto.json`.

## 9. Videos erzeugen

Der Stil steckt komplett im Repo:

| Was | Wo |
|---|---|
| Konzept, Regeln, Rapper-Pool | `docs/konzept.md` |
| Video-Skripte (Fragen, Prozente) | `content/videos/aNN.json`, erzeugt von `scripts/generate.py` |
| Look (Farben, Layout, Animation) | `video/src/Comparison.tsx` |
| Aussprache für die Stimme | `config/aussprache.json` |
| Bilder | `assets/` |
| Stimme | ElevenLabs "Adam", Modell eleven_multilingual_v2 (`scripts/build.py`) |

**Einfachster Weg: Claude Code im Web** (claude.ai/code) mit diesem Repo. Den ElevenLabs-Key dort in der Umgebung als Variable `ELEVENLABS_API_KEY` eintragen (Umgebungs-Menü in der Titelleiste, dann Edit). Dann z.B. sagen: "Erzeuge a51 bis a60 im gleichen Stil".

**Lokal auf dem Mac:**
```
echo 'ELEVENLABS_API_KEY=DEIN_KEY' > .env
cd video && npm install && cd ..
python scripts/build.py a51            # Stimme + Timeline (verbraucht ElevenLabs-Credits)
cd video && node scripts/render.mjs a51 && cd ..
python scripts/cut.py a51              # fertiges Video in out/cut/a51.mp4
```
`.env` ist in `.gitignore`, der Key landet nie auf GitHub.

**Credits:** Alle nutzen denselben ElevenLabs-Account. Ein Video kostet ca. 660 Zeichen. Vor großen Batches kurz absprechen.

## Regeln

- Nie `TK_cookies_*.json` oder `.env` teilen oder committen.
- Ein Konto wird immer nur von einer Person gleichzeitig hochgeladen.
- Neue Videos/Pläne per Pull Request, nicht direkt auf den Haupt-Branch.
