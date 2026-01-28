import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def bandpass_filter(signal, fs, low=0.5, high=40):
    """
    Filtr pasmowo-przepustowy dla sygnału EKG
    """
    nyq = 0.5 * fs
    b, a = butter(3, [low / nyq, high / nyq], btype="band")
    return filtfilt(b, a, signal)

def preprocess(time, signal, show_plot=True):
    fs = int(1 / np.mean(np.diff(time)))
    filtered = bandpass_filter(signal, fs)

    if show_plot:
        plt.figure(figsize=(10, 4))
        # plt.plot(time, signal, label="Oryginalny sygnał", alpha=0.6)
        plt.plot(time, filtered, label="Po filtracji", linewidth=1.5)
        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda")
        plt.title("Sygnał EKG – przed i po filtracji")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return fs, filtered
