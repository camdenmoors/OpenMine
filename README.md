# passive-https-collection
Passive HTTPS data fingerprinting and collection using HTTP Toolkit.


## Setup:
The included script is built for my use (collecting data from specific apps, and posting to Apache Solr), however, it can be edited to add your own fingerprints and data stores.

This tool depends on [HTTP Toolkit](https://httptoolkit.tech/) to setup the HTTP(S) interception, which it hooks into the GraphQL over Websocket interface it exposes.

To get started:
 - Install and run [HTTP Toolkit](https://httptoolkit.tech/)
 - Point a device with the HTTP toolkit certificate installed towards the interception server
 - Edit `fingerprinting.py`:
   - Update the `fingerprints` dictionary, where keys are the types of data, and the values are the keys the program should look for
   - Update `MINIMUM_FINGERPRINTS` if needed, this is the minimum number of keys found to mark the input data as a hit
 - Edit `main.py`:
   - Add your `SOLR_HOST` (see [this](https://solr.apache.org/) if you are unfamiliar), `TARGET_HOSTNAME` (the hostname if the API you would like to collect data from)
 - Start `main.py`
   - If needed, print out `foundItem`s to update your database schema
