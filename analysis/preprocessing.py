import numpy as np
import neurokit2 as nk

def preprocess_ecg(time, signal):
    fs = int(1 / np.mean(np.diff(time)))

    signals, info = nk.ecg_process(signal, sampling_rate=fs)

    rpeaks = info["ECG_R_Peaks"]
    rr_intervals = np.diff(time[rpeaks]) * 1000  # ms

    return {
        "fs": fs,
        "rpeaks": rpeaks,
        "rr": rr_intervals,
        "clean_signal": signals["ECG_Clean"]
    }
