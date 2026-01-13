import numpy as np

def detect_events(time, rpeaks, rr):
    events = []

    for i, rr_i in enumerate(rr):
        t = time[rpeaks[i]]

        if rr_i > 2000:
            events.append({
                "time": t,
                "type": "pause",
                "reason": "RR > 2s"
            })

        if rr_i < 400:
            events.append({
                "time": t,
                "type": "tachy",
                "reason": "RR < 400ms"
            })

    if len(rr) > 10:
        if np.std(rr) / np.mean(rr) > 0.15:
            events.append({
                "time": time[rpeaks[len(rpeaks)//2]],
                "type": "arrhythmia",
                "reason": "RR irregularity"
            })

    return events
