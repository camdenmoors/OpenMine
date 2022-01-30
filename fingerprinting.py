## Example fields
fingerprints = {
    'comment': ['id', ...],
    'user': ['id', ...],
    'post': ['id', ...]
}

MINIMUM_FINGERPRINTS = 3

def fingerprintData(data: dict):
    matchCounts = {
    }
    for fingerprint in fingerprints:
        matchCounts[fingerprint] = 0
        for field in fingerprints[fingerprint]:
            if field in data:
                matchCounts[fingerprint] += 1
    match = max(matchCounts, key=matchCounts.get)
    if matchCounts[match] >= MINIMUM_FINGERPRINTS:
        return match
    else:
        return False
