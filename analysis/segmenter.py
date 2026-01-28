def build_segments(events, window=1):
    """
    Budowanie przedziałów czasowych do weryfikacji przez lekarza
    """
    segments = []

    for t, reason in events:
        segments.append({
            "start": max(0, t - window),
            "end": t + window,
            "reasons": {reason}   # SET
        })

    segments.sort(key=lambda x: x["start"])

    merged = []
    for seg in segments:
        if not merged or seg["start"] > merged[-1]["end"]:
            merged.append(seg)
        else:
            merged[-1]["end"] = max(merged[-1]["end"], seg["end"])
            merged[-1]["reasons"].update(seg["reasons"])

    # konwersja set → list (JSON-friendly)
    for m in merged:
        m["reasons"] = sorted(list(m["reasons"]))

    return merged
