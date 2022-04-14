from modules.base import BaseProducerClass
from graphql_client import GraphQLClient
import traceback
import modules.https.fingerprints
import json
import base64
import brotli
import zlib

# Used to subcribe for http request creation and response
HTTP_TOOLKIT_SUBSCRIPTIONS = ["subscription OnRequest { requestReceived { id, matchedRuleId protocol, method, url, path, remoteIpAddress, hostname, headers, body, timingEvents httpVersion tags } }", "subscription OnResponse { responseCompleted { id, statusCode, statusMessage, headers, body, timingEvents tags } }"]

class HTTPSInterceptionModule(BaseProducerClass):
    targetHostnames = []
    fingerprints = {}
    # Requests are kept track of by UUID (this is limitation(?) of HTTP Toolkit, it works but it slows down their app when you leave it open in the background and come back with >10k requests)
    requestCache = {}

    def loadFingerprintModules(self, module):
        targetHostnames = []
        fingerprintModules = {}
        for fingerprintName, fingerprintModule in module.modules.items():
            try:
                module = fingerprintModule()
                fingerprintModules[module['hostname']] = module
                targetHostnames.append(module['hostname'])
                if('hostname' not in module or type(module['hostname']) != str):
                    raise Exception("Module has no hostname")
                if('name' not in module or type(module['hostname']) != str):
                    raise Exception("Module has no name")
                if 'fingerprints' not in module or type(module['fingerprints']) != dict:
                    raise Exception("Module has invalid fingerprints")
                if 'minMatches' not in module or type(module['minMatches']) != int:
                    raise Exception("Module has invalid minimum fingerprint count")
                self.log(f"Loaded fingerprint module {fingerprintName} - Hostname: {module['hostname']} - Minimum Matches: {module['minMatches']}")
            except Exception as e:
                self.log(f"Failed to load fingerprint module {fingerprintName}:")
                print(traceback.format_exc())
                raise e
        return [targetHostnames, fingerprintModules]

    # Request or Response recieved callback
    def callback(self, _id, data):
        if("requestReceived" in data['payload']['data']):
            requestData = data['payload']['data']['requestReceived']
            requestData['headers'] = json.loads(requestData['headers'])
            requestId = requestData['id']
            self.requestCache[requestId] = requestData
        elif ("responseCompleted" in data['payload']['data']):
            try:
                responseData = data['payload']['data']['responseCompleted']
                requestId = responseData['id']
                responseData['headers'] = json.loads(responseData['headers'])
                responseData['request'] = self.requestCache[requestId]
                requestURL = responseData['request']['url']
                hostname = responseData['request']['headers']['host']
                responseBody = responseData['body']
                del responseData['body']
                # Decode body
                try:
                    responseBody = brotli.decompress(base64.b64decode(responseBody))
                except:
                    try:
                        responseBody = zlib.decompress(base64.b64decode(responseBody), 16+zlib.MAX_WBITS)
                    except:
                        responseBody = base64.b64decode(responseBody)
                # If the hostname is in one of our moudles:
                if hostname in self.targetHostnames and 'repeat=false' not in requestURL:
                    matches = self.fingerprints[hostname]['method'](responseData, responseBody)
                    for matchType in matches:
                        self.log(f"Got {len(matches[matchType])} matches for {matchType}")
                        for event in matches[matchType]:
                            print(f"Sending event")
                            self.sendEvent(event)
                        
            except Exception as e:
                print(e)

    def run(self):
        self.targetHostnames, self.fingerprints = self.loadFingerprintModules(modules.https.fingerprints)
        ws = GraphQLClient('ws://127.0.0.1:45456/server/8000/subscription')
        for subscription in HTTP_TOOLKIT_SUBSCRIPTIONS:
            ws.subscribe(subscription, callback=self.callback)