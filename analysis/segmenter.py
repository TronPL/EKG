def build_segments(events, window=5):
    """
    Budowanie przedziałów czasowych do weryfikacji przez lekarza
    """
    segments = []

    for t, reason in events:
        segments.append({
            "start": max(0, t - window),
            "end": t + window,
            "reason": reason
        })

    segments.sort(key=lambda x: x["start"])

    merged = []
    for seg in segments:
        if not merged or seg["start"] > merged[-1]["end"]:
            merged.append(seg)
        else:
            merged[-1]["end"] = max(merged[-1]["end"], seg["end"])

    return merged
