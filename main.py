import pandas as pd
import json

from analysis.preprocessing import preprocess
from analysis.rpeaks import detect_r_peaks
from analysis.rules import detect_events
from analysis.segmenter import build_segments

# Wczytanie danych
df = pd.read_csv("data/example.csv")
time = df["time"].values
signal = df["voltage"].values

# Przetwarzanie
fs, clean_signal = preprocess(time, signal)
rpeaks = detect_r_peaks(clean_signal, fs)
events = detect_events(time, rpeaks)
segments = build_segments(events)

# Zapis wyników
with open("output/events.json", "w") as f:
    json.dump(segments, f, indent=4)

print("Fragmenty zapisu EKG wymagające sprawdzenia:")
for s in segments:
    print(s)
