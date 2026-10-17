import glob, time, torch, librosa, numpy as np, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from chatterbox.models.s3tokenizer import S3_SR
from chatterbox.models.s3gen import S3GEN_SR
R = "/home/user/comparison/samples/"
D = R + "free_tts/"
REF = R + "flash/eleven_multilingual_v2.mp3"
ALL = [f for f in glob.glob(R + "**/*.mp3", recursive=True) if "free_tts" not in f]
TEXTS = ["Rapper-Duell. Eine Nacht mit Nizi oder nie wieder Lucio hören? Schreib es in die Kommentare.",
         "Wer gewinnt? Kalim oder Ufo? Nur einer holt sich die Krone. Schick das deinem besten Freund!"]
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")

def boosted(exag):
    m.prepare_conditionals(REF, exaggeration=exag)
    wavs16 = [librosa.effects.trim(librosa.load(f, sr=S3_SR)[0], top_db=30)[0] for f in ALL]
    print(len(wavs16), "Clips,", round(sum(len(w) for w in wavs16) / S3_SR), "s Adam gesamt", flush=True)
    m.conds.t3.speaker_emb = torch.from_numpy(m.ve.embeds_from_wavs(wavs16, sample_rate=S3_SR)).mean(0, keepdim=True)
    long = [torch.from_numpy(w).unsqueeze(0) for w in wavs16 if len(w) > 2 * S3_SR]
    xv = torch.cat([m.s3gen.speaker_encoder.inference(w) for w in long]).mean(0, keepdim=True)
    m.conds.gen["embedding"] = xv

VARIANTS = [  # name, mehr Daten?, exaggeration, cfg_weight, temperature
    ("v1_wie_vorher", False, 0.5, 0.5, 0.8),
    ("v2_mehr_daten", True, 0.5, 0.5, 0.8),
    ("v3_mehr_daten_ruhiger", True, 0.4, 0.5, 0.6),
    ("v4_mehr_daten_energischer", True, 0.7, 0.3, 0.8),
]
for name, more, ex, cfg, temp in VARIANTS:
    boosted(ex) if more else m.prepare_conditionals(REF, exaggeration=ex)
    parts = []
    for t in TEXTS:
        torch.manual_seed(1)
        parts += [m.generate(t, language_id="de", exaggeration=ex, cfg_weight=cfg, temperature=temp), torch.zeros(1, int(0.5 * m.sr))]
    ta.save(D + f"klon_{name}.wav", torch.cat(parts, 1), m.sr)
    print(name, "fertig", flush=True)
