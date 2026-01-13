def build_segments(events, window=5):
    segments = []

    for e in events:
        segments.append({
            "start": max(0, e["time"] - window),
            "end": e["time"] + window,
            "reason": e["reason"]
        })

    segments.sort(key=lambda x: x["start"])

    merged = []
    for s in segments:
        if not merged or s["start"] > merged[-1]["end"]:
            merged.append(s)
        else:
            merged[-1]["end"] = max(merged[-1]["end"], s["end"])

    return merged
