
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

def uploadData(data: dict):
    print(data)

def getModule(host: str):
    return {
        "host": host,
        "name": "Apache Solr",
        "handleData": uploadData
    }

