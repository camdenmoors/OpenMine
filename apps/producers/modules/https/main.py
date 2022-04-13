from utilities import loadDatastoreModules, loadFingerprintModules
from graphql_client import GraphQLClient
import ..datastores
import fingerprints
import threading
import json
import base64
import brotli
import zlib

targetHostnames, fingerprintModules = loadFingerprintModules(fingerprints)
datastoreModules = loadDatastoreModules(datastores)

requestCache = {}

def callback(_id, data):
  if("requestReceived" in data['payload']['data']):
    requestData = data['payload']['data']['requestReceived']
    requestData['headers'] = json.loads(requestData['headers'])
    requestId = requestData['id']
    requestCache[requestId] = requestData
  elif ("responseCompleted" in data['payload']['data']):
    try:
      responseData = data['payload']['data']['responseCompleted']
      requestId = responseData['id']
      responseData['headers'] = json.loads(responseData['headers'])
      responseData['request'] = requestCache[requestId]
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
      if hostname in targetHostnames and 'repeat=false' not in requestURL:
        threading.Thread(target=fingerprintModules[hostname]['method'], args=[responseBody, datastoreModules]).start()
    except Exception as e:
      print(e)

if __name__ == '__main__':
  ws = GraphQLClient('ws://127.0.0.1:45456/server/8000/subscription')
  subscriptions = ["subscription OnRequest { requestReceived { id, matchedRuleId protocol, method, url, path, remoteIpAddress, hostname, headers, body, timingEvents httpVersion tags } }", "subscription OnResponse { responseCompleted { id, statusCode, statusMessage, headers, body, timingEvents tags } }"]
  for subscription in subscriptions:
    sub_id = ws.subscribe(subscription, callback=callback)
