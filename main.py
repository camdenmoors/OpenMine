from utilities import loadDatastoreModules, loadFingerprintModules
from graphql_client import GraphQLClient
import datastores
import fingerprints
import threading
import json
import base64
import brotli
import zlib

targetHostnames, fingerprintModules = loadFingerprintModules(fingerprints)
datastoreModules = loadDatastoreModules(datastores)

ws = GraphQLClient('ws://127.0.0.1:45456/server/8000/subscription')
requestCache = {}

def extractIDItems(data):
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
      if hostname in targetHostnames:
        extractedItems = extractIDItems(json.loads(responseBody))
        threading.Thread(target=fingerprintModules[hostname]['method'], args=(extractedItems, datastoreModules)).start()
    except Exception as e:
      print(e)

subscriptions = ["subscription OnRequest { requestReceived { id, matchedRuleId protocol, method, url, path, remoteIpAddress, hostname, headers, body, timingEvents httpVersion tags } }", "subscription OnResponse { responseCompleted { id, statusCode, statusMessage, headers, body, timingEvents tags } }"]

for subscription in subscriptions:
  sub_id = ws.subscribe(subscription, callback=callback)
