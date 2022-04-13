import json
from event import Event

HOSTNAME = "api.ifunny.mobi"
MINIMUM_MATCHES = 3

# Keys should be the table or core name in your database
FINGERPRINTS = {
    'ifunny-comments': ['id', 'cid', 'is_reply'],
    'ifunny-users': ['id', 'nick', 'photo', 'is_verified', 'original_nick'],
    'ifunny-posts': ['id', 'type', 'url', 'share_url', 'date_creation']
}

# Extract objects where 'id' is present
def preprocessData(data: dict):
    extractedItems = []

    def item_generator(json_input, lookup_key):
        if isinstance(json_input, dict):
            for k, v in json_input.items():
                if k == lookup_key:
                    extractedItems.append(json_input)
                else:
                    item_generator(v, lookup_key)
        elif isinstance(json_input, list):
            for item in json_input:
                item_generator(item, lookup_key)
    item_generator(data, 'id')
    return extractedItems
    

def fingerprintData(responseData: str):
    extractedData = preprocessData(json.loads(responseData))
    matches = {}
    # Fill matches with empty arrays based off of fingerprints
    for fingerprint in FINGERPRINTS:
        matches[fingerprint] = []
    # Match data from fingerprints
    for object in extractedData:
        event = Event(raw=json.dumps(object), producer="https")
        uniqueKeys = {k: v for k, v in object.items() if type(v) is not dict}
        if 'user' in object and 'id' in object['user']:
            uniqueKeys['user_id'] = object['user']['id']
            uniqueKeys['username'] = object['user']['nick']
        if 'num' in object:
            if 'subscriptions' in object['num']:
                uniqueKeys['numSubscriptions'] = object['num']['subscriptions']
            if 'subscribers' in object['num']:
                uniqueKeys['statistics.followers'] = object['num']['subscribers']
            if 'smiles' in object['num']:
                uniqueKeys['statistics.positive'] = object['num']['smiles']
            if 'unsmiles' in object['num']:
                uniqueKeys['statistics.negative'] = object['num']['unsmiles']
            if 'comments' in object['num']:
                uniqueKeys['statistics.interactions'] = object['num']['comments']
            if 'views' in object['num']:
                uniqueKeys['statistics.views'] = object['num']['views']
            if 'republished' in object['num']:
                uniqueKeys['statistics.republish'] = object['num']['republished']

        matchCounts = {}
        for fingerprint in FINGERPRINTS:
            matchCounts[fingerprint] = 0
            for field in FINGERPRINTS[fingerprint]:
                if field in object:
                    matchCounts[fingerprint] += 1
        match = max(matchCounts, key=matchCounts.get)
        if matchCounts[match] >= MINIMUM_MATCHES:
            matches[match].append(uniqueKeys)
    
    return matches

def getModule():
    return {
        "name": "iFunny",
        "hostname": HOSTNAME,
        "fingerprints": FINGERPRINTS,
        "minMatches": MINIMUM_MATCHES,
        "method": fingerprintData
    }