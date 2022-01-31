HOSTNAME = "api.ifunny.mobi"
MINIMUM_MATCHES = 3

# Keys should be the table or core name in your database
FINGERPRINTS = {
    'ifunny-comments': ['id', 'cid', 'is_reply'],
    'ifunny-users': ['id', 'nick', 'photo', 'is_verified', 'original_nick'],
    'ifunny-posts': ['id', 'type', 'url', 'share_url', 'date_creation']
}


def fingerprintData(extractedData: list, datastoreModules: list):
    print(extractedData)
    matches = {}
    # Fill matches with empty arrays based off of fingerprints
    for fingerprint in FINGERPRINTS:
        matches[fingerprint] = []
    # Match data from fingerprints
    for object in extractedData:
        matchCounts = {}
        for fingerprint in FINGERPRINTS:
            matchCounts[fingerprint] = 0
            for field in FINGERPRINTS[fingerprint]:
                if field in object:
                    matchCounts[fingerprint] += 1
        match = max(matchCounts, key=matchCounts.get)
        if matchCounts[match] >= MINIMUM_MATCHES:
            matches[match].append(object)
    for datastoreModule in datastoreModules:
        datastoreModule['handleData'](matches)


def getModule():
    return {
        "name": "iFunny",
        "hostname": HOSTNAME,
        "fingerprints": FINGERPRINTS,
        "minMatches": MINIMUM_MATCHES,
        "method": fingerprintData
    }

