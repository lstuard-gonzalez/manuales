import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = m.transcribe(__import__("numpy").frombuffer(open(sys.argv[1],"rb").read(), dtype="int16").astype("float32")/32768.0, language="es", beam_size=5, vad_filter=True)
for s in segs:
    print(f"[{s.start:5.1f}] {s.text.strip()}")
