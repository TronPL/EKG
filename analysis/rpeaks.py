import numpy as np
from scipy.signal import find_peaks

def detect_r_peaks(signal, fs):
    """
    Prosta detekcja załamków R na podstawie amplitudy i odstępu czasowego
    """
    distance = int(0.3 * fs)  # min. 300 ms
    peaks, _ = find_peaks(signal, distance=distance, height=np.mean(signal))
    return peaks
