import numpy as np
import pandas as pd

# Parametry symulowanego EKG
fs = 250  # Hz (próbkowanie co 4 ms)
duration = 120  # sekundy, 2 minuty
t = np.arange(0, duration, 1/fs)

# Symulacja bazowego EKG (regularne R-peaki co 0.857 s ~ 70 bpm)
hr = 70  # bpm
rr_interval = 60 / hr  # s
r_peak_times = np.arange(0, duration, rr_interval)
signal = 0.05 * np.sin(2 * np.pi * 1 * t)  # baseline

# Wstawianie R-peaków
for rp in r_peak_times:
    idx = int(rp * fs)
    if idx < len(signal):
        signal[idx] += 1.0

# Dodanie arytmii
# 1. Pauza w 30 s (RR ~ 2.5 s)
pause_idx = int((30 + 0.5) * fs)
signal[pause_idx] += 1.0  # dodatkowy R-peak po 2.5 s

# 2. PAC / PVC co 15 s
for pac_time in [15, 45, 75, 105]:
    idx = int(pac_time * fs)
    if idx < len(signal):
        signal[idx] += 0.8  # trochę mniejszy R-peak

# 3. AF podejrzenie w 90-100 s (bardzo nieregularne RR)
af_start = 90
af_end = 100
af_rr = np.random.uniform(0.6, 1.0, size=int((af_end-af_start)/rr_interval))
af_times = af_start + np.cumsum(af_rr)
for rp in af_times:
    idx = int(rp * fs)
    if idx < len(signal):
        signal[idx] += 1.0

# Tworzenie DataFrame
df = pd.DataFrame({
    "time": t,
    "voltage": signal
})

# Zapis CSV
csv_path = "simulated_ecg_with_arrhythmia.csv"
df.to_csv(csv_path, index=False)
csv_path
