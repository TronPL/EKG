import pandas as pd
import json

from analysis.preprocessing import preprocess_ecg
from analysis.rules import detect_events
from analysis.segmenter import build_segments

# Wczytaj dane
df = pd.read_csv("data/example.csv")
time = df["time"].values
signal = df["voltage"].values

# Analiza
data = preprocess_ecg(time, signal)

events = detect_events(
    time,
    data["rpeaks"],
    data["rr"]
)

segments = build_segments(events)

# Zapis
with open("output/events.json", "w") as f:
    json.dump(segments, f, indent=4)

print("Zaznaczone fragmenty do sprawdzenia:")
for s in segments:
    print(s)
