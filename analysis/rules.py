import numpy as np

"""
Regułowy detektor arytmii z jednokanałowego Holtera ECG
UWAGA: screening (podejrzenia, nie diagnoza)
Jednostki:
- time: sekundy
- RR: milisekundy
"""

# =====================================================
# RR
# =====================================================

def compute_rr(time, rpeaks):
    """
    time   : ndarray czasu [s]
    rpeaks : indeksy R-peaków
    """
    rr = np.diff(time[rpeaks]) * 1000  # RR [ms]
    rr_t = time[rpeaks[1:]]            # czas przypisany do RR
    return rr, rr_t


# =====================================================
# Pauzy / Bradykardia
# =====================================================

def detect_pauses(rr, rr_t, rr_pause=2000, rr_brady=1200):
    events = []

    for r, t in zip(rr, rr_t):
        if r > rr_pause:
            events.append((t, "pauza rytmu (RR > 2.0 s)"))
        elif r > rr_brady:
            events.append((t, "bradykardia zatokowa"))

    return events


# =====================================================
# Tachykardia
# =====================================================

def detect_tachycardia(rr, rr_t, rr_tachy=400):
    events = []

    for r, t in zip(rr, rr_t):
        if r < rr_tachy:
            events.append((t, "tachykardia"))

    return events


# =====================================================
# Skurcze przedwczesne (PAC / PVC)
# =====================================================

def detect_premature_beats(rr, rr_t):
    events = []

    if len(rr) < 3:
        return events

    mean_rr = np.mean(rr)

    for i in range(len(rr) - 1):
        if rr[i] < 0.8 * mean_rr and rr[i + 1] > 1.2 * mean_rr:
            events.append((rr_t[i], "podejrzenie skurczu przedwczesnego (PAC/PVC)"))

    return events


# =====================================================
# Bigeminia
# =====================================================

def detect_bigeminy(rr, rr_t):
    events = []

    if len(rr) < 6:
        return events

    m = np.mean(rr)

    for i in range(len(rr) - 3):
        p = rr[i:i + 4]
        if (
            p[0] < 0.8 * m and p[1] > 1.2 * m and
            p[2] < 0.8 * m and p[3] > 1.2 * m and
            np.std(p) > 50
        ):
            events.append((rr_t[i], "podejrzenie bigeminii"))

    return events


# =====================================================
# SVT (podejrzenie)
# =====================================================

def detect_svt(rr, rr_t, min_beats=8):
    events = []

    if len(rr) < min_beats:
        return events

    for i in range(len(rr) - min_beats):
        window = rr[i:i + min_beats]
        if np.mean(window) < 400 and np.std(window) < 30:
            events.append((rr_t[i], "SVT (podejrzenie)"))

    return events


# =====================================================
# Migotanie przedsionków (AF) – OKNA
# =====================================================

def detect_af(rr, rr_t, window_s=30):
    events = []

    if len(rr) < 10:
        return events

    start = 0
    while start < len(rr):
        end = start
        while end < len(rr) and rr_t[end] - rr_t[start] < window_s:
            end += 1

        window = rr[start:end]
        if len(window) >= 10:
            cv = np.std(window) / np.mean(window)
            rmssd = np.sqrt(np.mean(np.diff(window) ** 2))

            if cv > 0.20 and rmssd > 80:
                events.append((rr_t[start], "migotanie przedsionków (AF – podejrzenie)"))

        start = end

    return events


# =====================================================
# Wenckebach (Mobitz I) – heurystyka
# =====================================================

def detect_wenckebach(rr, rr_t):
    events = []

    if len(rr) < 4:
        return events

    for i in range(len(rr) - 3):
        r = rr[i:i + 4]
        if (
            r[0] > r[1] > r[2] and
            r[3] > 1.5 * np.mean(r[:3])
        ):
            events.append((rr_t[i + 3], "blok AV II° (Wenckebach – podejrzenie)"))

    return events


# =====================================================
# GŁÓWNY PIPELINE
# =====================================================

def detect_arrhythmias(time, rpeaks):
    if len(rpeaks) < 5:
        return []

    rr, rr_t = compute_rr(time, rpeaks)

    events = []
    events.extend(detect_pauses(rr, rr_t))
    events.extend(detect_tachycardia(rr, rr_t))
    events.extend(detect_premature_beats(rr, rr_t))
    events.extend(detect_bigeminy(rr, rr_t))
    events.extend(detect_svt(rr, rr_t))
    events.extend(detect_af(rr, rr_t))
    events.extend(detect_wenckebach(rr, rr_t))

    events.sort(key=lambda x: x[0])
    return events
