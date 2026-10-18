# Setup für Windows

Gleiches Ziel wie [SETUP.md](SETUP.md) (Mac), nur mit Windows-Befehlen. Einmalig ca. 20 Minuten.

## 1. Zugang

1. GitHub-Einladung zum Repo `neinkob12/comparison` annehmen (Mail von GitHub).
2. Den ElevenLabs-Key bekommst du **privat** von Jakob (nie in einen Gruppenchat, nie ins Repo).

## 2. Werkzeuge installieren

Startmenü, **"Terminal"** oder **"PowerShell"** öffnen und Zeile für Zeile einfügen (jeweils mit "Y"/"Ja" bestätigen):
```
winget install --id Git.Git -e
winget install --id GitHub.cli -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Gyan.FFmpeg -e
winget install --id Anaconda.Miniconda3 -e
setx PYTHONUTF8 1
```
`setx PYTHONUTF8 1` sorgt dafür, dass Umlaute und Emojis richtig gelesen werden.

Danach **das Terminal schließen**. Ab jetzt immer über das Startmenü **"Anaconda Prompt (miniconda3)"** arbeiten, nicht im normalen Terminal.

## 3. Repo holen

Im **Anaconda Prompt**:
```
git config --global user.name "Dein Name"
git config --global user.email "deine@mail.de"
gh auth login
cd %USERPROFILE%
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
```

Dann den Login-Teil einrichten. Diese Zeile zeigt den Ordner an:
```
python -c "import tiktokautouploader, os; print(os.path.dirname(tiktokautouploader.__file__))"
```
Mit dem angezeigten Pfad (Beispiel, deiner sieht ähnlich aus):
```
cd /d C:\Users\DEINNAME\miniconda3\envs\tiktok\Lib\site-packages\tiktokautouploader\Js_assets
npm install
```

## 5. TikTok-Konto einloggen (einmal pro Konto)

**Wichtig:** Der QR-Code loggt das Konto ein, das **gerade in der TikTok-App auf deinem Handy offen ist**. Vorher in der App auf das richtige Konto wechseln.

Im gleichen Ordner wie eben (`...\Js_assets`):
```
node login.js
```
Einloggen. Das Fenster schließt sich, sobald du auf der For-You-Seite bist (sonst `tiktok.com/foryou` eintippen). Dann, mit dem Kontonamen aus `config\accounts.json`:
```
move TK_cookies.json %USERPROFILE%\comparison\TK_cookies_KONTO.json
cd /d %USERPROFILE%\comparison
```
Die Datei `TK_cookies_KONTO.json` ist wie ein Passwort: nie teilen, sie ist in `.gitignore`.

## 6. Jeden Tag / jede Session

**Anaconda Prompt** öffnen:
```
cd /d %USERPROFILE%\comparison
conda activate tiktok
git pull
```

## 7. Hochladen

```
python scripts\tiktok_upload.py status
python scripts\tiktok_upload.py test a17 --account KONTO
python scripts\tiktok_upload.py plan a17 a50 --account KONTO
python scripts\tiktok_upload.py mark a01 a16 --account KONTO
```
| Befehl | Was er macht |
|---|---|
| `status` | Wer hat was eingeplant, wie viele Tage sind abgedeckt |
| `test` | 1 Video als Entwurf (zum Prüfen) |
| `plan` | einplanen laut Plan, max. 10 Tage voraus |
| `mark` | von Hand gepostete Videos als erledigt eintragen |

Pro Video macht das Script: Video, Beschreibung, Hashtags, Sound aus den Favoriten (Lautstärke + Fade-in), Cover, KI-Kennzeichnung, Uhrzeit. Klappt ein Schritt nicht automatisch, hält es an und sagt, was du im Browser von Hand machen sollst, dann Enter im Prompt.

Videos gehören nach `out\cut\` (z.B. `out\cut\a17.mp4`). Ordner anlegen und öffnen:
```
mkdir out\cut
explorer out\cut
```

**Tracking:** Jeder Upload landet in `docs\upload_log.csv` und wird automatisch nach GitHub gepusht. Schon eingeplante Videos werden übersprungen, deshalb vorher immer `git pull`. Den Sound vorher in der TikTok-App für das Konto **favorisieren**.

## 8. Videos erzeugen

Was wo liegt (Stil, Skripte, Bilder) und wie man ein neues Konto anlegt: siehe [SETUP.md](SETUP.md), Abschnitte 8 und 9.

**Einfachster Weg: Claude Code im Web** (claude.ai/code) mit diesem Repo, Key dort in der Umgebung als `ELEVENLABS_API_KEY` eintragen. Dann z.B.: "Erzeuge a51 bis a60 im gleichen Stil".

**Lokal unter Windows:**
```
echo ELEVENLABS_API_KEY=DEIN_KEY> .env
cd video
npm install
cd ..
python scripts\build.py a51
cd video
node scripts\render.mjs a51
cd ..
python scripts\cut.py a51
```
Fertiges Video: `out\cut\a51.mp4`. Wichtig: bei `echo` **kein Leerzeichen** vor `>`, sonst hängt eins am Key.

## Häufige Probleme

| Meldung | Lösung |
|---|---|
| `'conda' is not recognized` | Nicht im normalen Terminal, sondern im **Anaconda Prompt** arbeiten |
| `'git'/'node'/'ffmpeg' is not recognized` | Anaconda Prompt schließen und neu öffnen (nach der Installation nötig) |
| `No module named 'tiktokautouploader'` | `conda activate tiktok` vergessen |
| `ERROR: SOUND ... NOT FOUND` | Sound in der TikTok-App für dieses Konto favorisieren, Stichwort in `config\accounts.json` prüfen |
| Login-Fenster öffnet sich nicht | Schritt 4 (`npm install` im Js_assets-Ordner) wiederholen |

## Regeln

- Nie `TK_cookies_*.json` oder `.env` teilen oder committen.
- Ein Konto wird immer nur von einer Person gleichzeitig hochgeladen.
- Neue Videos/Pläne per Pull Request, nicht direkt auf den Haupt-Branch.
