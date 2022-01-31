import requests
import json

# Data comes in this format:
# {
#   "table-name": [
#       {
#           "id": "..."
#           "name": "..."
#           ...
#       }
#   ]
# }
# Were table names are defined by the fingerprint files

solrConfig = {
    "hostname": "",
    "port": ""
}

def uploadData(data: dict):
    for core in data:
        if len(data[core]) > 0:
            response = requests.post(f"http://{solrConfig['hostname']}:{solrConfig['port']}/solr/{core}/update?commitWithin=1000&overwrite=true&wt=json", data=json.dumps(data[core]), headers={'Content-Type': 'application/json'})
            if(response.status_code == 200):
                print(f"Added {str(len(data[core]))} documents to {core}")
            else:
                print(response.text)

def getModule(config: dict):
    solrConfig["hostname"] = config["hostname"]
    solrConfig["port"] = config["port"]
    return {
        "host": config["hostname"],
        "name": "Apache Solr",
        "handleData": uploadData
    }

