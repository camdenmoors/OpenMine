from modules.base import BaseProducerClass
from graphql_client import GraphQLClient
import traceback
import modules.https.fingerprints

import json
import base64
import zlib
import brotli


# Used to subcribe for http request creation and response
HTTP_TOOLKIT_SUBSCRIPTIONS = [
    "subscription OnRequest { requestReceived { id, matchedRuleId protocol, method, url, path, remoteIpAddress, hostname, headers, body, timingEvents httpVersion tags } }",
    "subscription OnResponse { responseCompleted { id, statusCode, statusMessage, headers, body, timingEvents tags } }",
    "subscription OnWebSocketMessageReceived { webSocketMessageReceived { streamId direction content isBinary eventTimestamp timingEvents tags } }",
    "subscription OnWebSocketMessageSent { webSocketMessageSent { streamId direction content isBinary eventTimestamp timingEvents tags } }",
    "subscription OnRuleEvent { ruleEvent { requestId ruleId eventType eventData } }",
]


class HTTPSInterceptionModule(BaseProducerClass):
    targetHostnames = []
    fingerprints = {}
    # Requests are kept track of by UUID (this is limitation(?) of HTTP Toolkit, it works but it slows down their app when you leave it open in the background and come back with >10k requests)
    requestCache = {}
    websocket_streams = {}
    gateway_intercepts = {}

    def loadFingerprintModules(self, module):
        print("Loading fingerprint modules...")
        targetHostnames = []
        fingerprintModules = {}
        for fingerprintName, fingerprintModule in module.modules.items():
            self.log(f"Loading fingerprint module {fingerprintName}...")
            try:
                module = fingerprintModule()
                fingerprintModules[module["hostname"]] = module
                targetHostnames.append(module["hostname"])
                if "hostname" not in module or type(module["hostname"]) != str:
                    raise Exception("Module has no hostname")
                if "name" not in module or type(module["hostname"]) != str:
                    raise Exception("Module has no name")
                if "method" not in module or (type(module["method"]) != str and not callable(module["method"])):
                    raise Exception("Module has no method")
                if module["method"] != "WS":
                    if "fingerprints" not in module or type(module["fingerprints"]) != dict:
                        raise Exception("Module has invalid fingerprints")
                    if "minMatches" not in module or type(module["minMatches"]) != int:
                        raise Exception("Module has invalid minimum fingerprint count")
                self.log(
                    f"Loaded fingerprint module {fingerprintName} - Hostname: {module['hostname']}"
                )
            except Exception as e:
                self.log(f"Failed to load fingerprint module {fingerprintName}:")
                print(traceback.format_exc())
                raise e
        return [targetHostnames, fingerprintModules]

    # Request or Response recieved callback
    def callback(self, _id, data):
        if "requestReceived" in data["payload"]["data"]:
            requestData = data["payload"]["data"]["requestReceived"]
            requestData["headers"] = json.loads(requestData["headers"])
            requestId = requestData["id"]
            self.requestCache[requestId] = requestData
        elif "responseCompleted" in data["payload"]["data"]:
            try:
                responseData = data["payload"]["data"]["responseCompleted"]
                requestId = responseData["id"]
                responseData["headers"] = json.loads(responseData["headers"])
                responseData["request"] = self.requestCache[requestId]
                requestURL = responseData["request"]["url"]
                hostname = responseData["request"]["headers"]["host"]
                responseBody = responseData["body"]
                del responseData["body"]
                # Decode body
                try:
                    responseBody = brotli.decompress(base64.b64decode(responseBody))
                except:
                    try:
                        responseBody = zlib.decompress(
                            base64.b64decode(responseBody), 16 + zlib.MAX_WBITS
                        )
                    except:
                        responseBody = base64.b64decode(responseBody)

                # If the hostname is in one of our moudles:
                if (
                    hostname in self.targetHostnames
                    and "repeat=false" not in requestURL
                ):
                    matches = self.fingerprints[hostname]["method"](
                        responseData, responseBody
                    )
                    for matchType in matches:
                        self.log(
                            f"Got {len(matches[matchType])} matches for {matchType}"
                        )
                        for event in matches[matchType]:
                            print(f"Sending event")
                            self.sendEvent(event)
            except Exception as e:
                print(e)
        elif "webSocketMessageSent" in data["payload"]["data"] or "webSocketMessageReceived" in data["payload"]["data"]:
            wsData = data["payload"]["data"].get("webSocketMessageSent") or data["payload"]["data"].get("webSocketMessageReceived")

            streamId = wsData["streamId"]

            wsData["content"] = base64.b64decode(wsData["content"])
            wsData["isBinary"] = bool(wsData["isBinary"])
            wsData["direction"] = "sent"


            # Does this stream exist in the WebSocket streams?
            if streamId in self.gateway_intercepts:
                self.gateway_intercepts[streamId].handle_message(wsData["content"])
            else:
                self.log(f"WebSocket stream {streamId} not found in gateway intercepts")

        elif "ruleEvent" in data["payload"]["data"]:
            ruleEventData = data["payload"]["data"]["ruleEvent"]
            
            if ruleEventData["eventType"] == "passthrough-websocket-connect":
                requestId = ruleEventData["requestId"]
                hostname = ruleEventData["eventData"]["hostname"]

                self.websocket_streams[requestId] = ruleEventData["eventData"]
                self.log(
                    f"WebSocket connection established for request {requestId}: {ruleEventData['eventData']}"
                )

                if hostname in self.targetHostnames:
                    # Create new interceptor
                    self.log(f"Creating new interceptor for {hostname}: {requestId}")
                    self.gateway_intercepts[requestId] = self.fingerprints[hostname]["processingClass"](
                        ruleEventData['eventData']
                    )

    def run(self):
        self.targetHostnames, self.fingerprints = self.loadFingerprintModules(
            modules.https.fingerprints
        )
        ws = GraphQLClient(
            "ws://127.0.0.1:45456/session/d2060eb6-dce2-4f74-8266-a9335eaa178c/subscription"
        )
        for subscription in HTTP_TOOLKIT_SUBSCRIPTIONS:
            ws.subscribe(subscription, callback=self.callback)
