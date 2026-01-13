import numpy as np
from scipy.signal import butter, filtfilt

def bandpass_filter(signal, fs, low=0.5, high=40):
    """
    Filtr pasmowo-przepustowy dla sygnału EKG
    """
    nyq = 0.5 * fs
    b, a = butter(3, [low / nyq, high / nyq], btype="band")
    return filtfilt(b, a, signal)

def preprocess(time, signal):
    fs = int(1 / np.mean(np.diff(time)))
    filtered = bandpass_filter(signal, fs)
    return fs, filtered
