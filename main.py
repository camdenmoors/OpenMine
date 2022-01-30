from fingerprinting import fingerprintData
from graphql_client import GraphQLClient
import requests
import json
import base64
import brotli
import uuid
import zlib

SOLR_HOST = "YOUR_SOLR_IP"
TARGET_HOSTNAME = "YOUR_TARGET_HOSTNAME"

ws = GraphQLClient('ws://127.0.0.1:45456/server/8000/subscription')
requestCache = {}

def extractIDItems(data):
  extractedItems = []
  def item_generator(json_input, lookup_key):
      if isinstance(json_input, dict):
          for k, v in json_input.items():
              if k == lookup_key:
                uniqueKeys = {k: v for k, v in json_input.items() if type(v) is not dict}
                if 'user' in json_input and 'id' in json_input['user']:
                  uniqueKeys['user_id'] = json_input['user']['id']
                extractedItems.append(uniqueKeys)
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
      responseData['headers'] = json.loads(responseData['headers'])
      requestId = responseData['id']
      responseData['request'] = requestCache[requestId]
      responseBody = responseData['body']
      del responseData['body']
      try:
        responseBody = brotli.decompress(base64.b64decode(responseBody))
      except:
        try:
          responseBody = zlib.decompress(base64.b64decode(responseBody), 16+zlib.MAX_WBITS)
        except:
          responseBody = base64.b64decode(responseBody)
      if(responseData['request']['headers']['host'] == TARGET_HOSTNAME):
        try:
          userPayloads = []
          commentPayloads = []
          postPayloads = []
          for foundItem in extractIDItems(json.loads(responseBody)):
            try:
              fingerprint = fingerprintData(foundItem)
              if fingerprint:
                if(fingerprint == 'comment'):
                  commentPayloads.append(foundItem)
                elif(fingerprint == 'user'):
                  userPayloads.append(foundItem)
                elif(fingerprint == 'post'):
                  postPayloads.append(foundItem)
            except Exception as e:
              print(e)
          if userPayloads:
            response = requests.post(f"http://{SOLR_HOST}:8983/solr/users/update?commitWithin=1000&overwrite=true&wt=json", data=json.dumps(userPayloads), headers={'Content-Type': 'application/json'})
            if(response.status_code == 200):
              print(f"Added {str(len(userPayloads))} users")
            else:
              print(response.text)
          if commentPayloads:
            response = requests.post(f"http://{SOLR_HOST}:8983/solr/comments/update?commitWithin=1000&overwrite=true&wt=json", data=json.dumps(commentPayloads), headers={'Content-Type': 'application/json'})
            if(response.status_code == 200):
              print(f"Added {str(len(commentPayloads))} comments")
            else:
              print(response.text)
          if postPayloads:
            response = requests.post(f"http://{SOLR_HOST}:8983/solr/posts/update?commitWithin=1000&overwrite=true&wt=json", data=json.dumps(postPayloads), headers={'Content-Type': 'application/json'})
            if(response.status_code == 200):
              print(f"Added {str(len(postPayloads))} posts")
            else:
              print(response.text)
        except Exception as e:
          print(e)
    except:
      pass

subscriptions = ["subscription OnRequest { requestReceived { id, matchedRuleId protocol, method, url, path, remoteIpAddress, hostname, headers, body, timingEvents httpVersion tags } }", "subscription OnResponse { responseCompleted { id, statusCode, statusMessage, headers, body, timingEvents tags } }"]

for subscription in subscriptions:
  sub_id = ws.subscribe(subscription, callback=callback)
