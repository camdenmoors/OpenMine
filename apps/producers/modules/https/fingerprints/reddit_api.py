import json
import pydash
from uuid import uuid4

HOSTNAME = "gateway.reddit.com"
MINIMUM_MATCHES = 6

# Keys should be the table or core name in your database
FINGERPRINTS = {
    'reddit-posts': ['id', 'author', 'callToAction', 'created', 'flair', 'liveCommentsWebsocket', 'permalink'],
    'reddit-comments': ['id', 'authorId', 'media.richtextContent.document[0].c[0].t', 'media.richtextContent.document[0].c[0].t', 'media.richtextContent.document[0].c[0].t', 'media.richtextContent.document[0].c[0].t', 'media.richtextContent.document[0].c[0].t']
}

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


def fingerprintData(extractedData: str, datastoreModules: list):
    if extractedData:
        try:
            extractedData = preprocessData(json.loads(extractedData))
            matches = {}
            # Fill matches with empty arrays based off of fingerprints
            for fingerprint in FINGERPRINTS:
                matches[fingerprint] = []
            # Match data from fingerprints
            for object in extractedData:
                uniqueKeys = {k: v for k, v in object.items() if type(v) is not dict and type(v) is not list}
                if pydash.get(object, 'media.richtextContent.document[0].c[0].t') is not None:
                    uniqueKeys['text'] = pydash.get(object, 'media.richtextContent.document[0].c[0].t')
                matchCounts = {}
                for fingerprint in FINGERPRINTS:
                    matchCounts[fingerprint] = 0
                    for field in FINGERPRINTS[fingerprint]:
                        if pydash.get(object, field) is not None:
                            matchCounts[fingerprint] += 1
                match = max(matchCounts, key=matchCounts.get)
                if matchCounts[match] >= MINIMUM_MATCHES:
                    matches[match].append(uniqueKeys)
            for datastoreModule in datastoreModules:
                datastoreModule['handleData'](matches)
        except Exception as e:
            print(e)

def getModule():
    return {
        "name": "Reddit Gateway",
        "hostname": HOSTNAME,
        "fingerprints": FINGERPRINTS,
        "minMatches": MINIMUM_MATCHES,
        "method": fingerprintData
    }