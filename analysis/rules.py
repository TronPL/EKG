import numpy as np

"""
Regułowy detektor arytmii z jednokanałowego Holtera ECG
Autor: ---
UWAGA: system screeningowy (podejrzenia, nie diagnoza)
"""


# =====================================================
# Pomocnicze: RR
# =====================================================

def compute_rr(time, rpeaks):
    """
    time   : ndarray czasu w sekundach
    rpeaks : indeksy R-peaków
    """
    rr = np.diff(time[rpeaks]) * 1000      # RR w ms
    rr_t = time[rpeaks[1:]]                # czas przypisany do RR
    return rr, rr_t


# =====================================================
# Pauzy i bradykardia (Trzeba dorobić analizę w nocy bo tam niższy puls i może dać fałszywe alarmy)
# =====================================================

def detect_pauses(rr, rr_t, rr_pause=2000, rr_brady=1200):
    events = []

    for r, t in zip(rr, rr_t):
        if r > rr_pause:
            events.append((t, "pauza rytmu (RR > 2s)"))
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

    if len(rr) < 2:
        return events

    mean_rr = np.mean(rr)

    for i in range(len(rr) - 1):
        if rr[i] < 0.8 * mean_rr and rr[i + 1] > 1.2 * mean_rr:
            events.append((rr_t[i], "skurcz przedwczesny (PAC/PVC)"))

    return events


# =====================================================
# Bigeminia
# =====================================================

def detect_bigeminy(rr, rr_t):
    events = []

    if len(rr) < 4:
        return events

    m = np.mean(rr)

    for i in range(len(rr) - 3):
        p = rr[i:i + 4]
        if (p[0] < 0.8 * m and p[1] > 1.2 * m and
            p[2] < 0.8 * m and p[3] > 1.2 * m):
            events.append((rr_t[i], "bigeminia"))

    return events


# =====================================================
# SVT (podejrzenie)
# =====================================================

def detect_svt(rr, rr_t, min_beats=6):
    events = []

    if len(rr) < min_beats:
        return events

    for i in range(len(rr) - min_beats):
        window = rr[i:i + min_beats]
        if np.mean(window) < 400 and np.std(window) < 30:
            events.append((rr_t[i], "SVT (podejrzenie)"))

    return events


# =====================================================
# Migotanie przedsionków (AF)
# =====================================================

def detect_af(rr, rr_t):
    events = []

    if len(rr) < 10:
        return events

    cv = np.std(rr) / np.mean(rr)
    rmssd = np.sqrt(np.mean(np.diff(rr) ** 2))

    if cv > 0.20 and rmssd > 80:
        events.append((np.mean(rr_t), "migotanie przedsionków (AF)"))

    return events


# =====================================================
# Blok AV II° (Wenckebach) – heurystyka
# =====================================================

def detect_wenckebach(rr, rr_t):
    events = []

    if len(rr) < 4:
        return events

    for i in range(len(rr) - 3):
        r = rr[i:i + 4]
        if r[0] > r[1] > r[2] and r[3] > 1.5 * np.mean(r[:3]):
            events.append((rr_t[i + 3], "blok AV II° (Wenckebach?)"))

    return events
# =====================================================
# GŁÓWNY PIPELINE
# =====================================================

def detect_arrhythmias(time, rpeaks):
    """
    Zwraca listę:
    [(czas [s], opis zdarzenia), ...]
    """

    if len(rpeaks) < 3:
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

    # sortowanie po czasie
    events.sort(key=lambda x: x[0])
    return events