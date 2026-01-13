import numpy as np

def detect_events(time, rpeaks):
    """
    Reguły wykrywania potencjalnych anomalii rytmu serca
    """
    events = []
    rr_intervals = np.diff(time[rpeaks]) * 1000  # ms

    for i, rr in enumerate(rr_intervals):
        t = time[rpeaks[i]]

        if rr > 2000:
            events.append((t, "pauza rytmu (RR > 2s)"))

        if rr < 400:
            events.append((t, "tachykardia (RR < 400ms)"))

    if len(rr_intervals) > 10:
        if np.std(rr_intervals) / np.mean(rr_intervals) > 0.15:
            events.append((time[rpeaks[len(rpeaks)//2]],
                           "nieregularność rytmu (arytmia)"))

    return events
