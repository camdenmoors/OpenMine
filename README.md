# OpenMine
A framework for passive and active data collection.
![OpenMine](https://user-images.githubusercontent.com/66680985/162869975-5be6be3b-43d8-48c8-ac81-ef30a9dea091.jpg)

## Implementation:
Passive Producers:
 - [x] HTTP Interception & Fingerprinting
   - [ ] Interaction Generators
 - [x] WebSocket Collection

Active Producers:
 - [x] Active API Scraping Modules (AKA Data Expansion)
 - [ ] Web Scraping
 - [ ] ZMap (or similar)
 - [ ] ZGrab (or similar)

Consumers:
 - [x] Solr Integration
   - [x] Document Linking
 - [ ] BigQuery Integration
   - [ ] Document Linking (Not sure if possible, ~5s/query minimum. Maybe with non-free allocated capacity)
 - [ ] Cassandra Integration
   - [ ] Document Linking
 - [ ] Data Transformation (Common event structure)
 - [ ] AI Analysis 

## Setup:
This project is still a work in progress and does not have a simple setup procedure.

### Passive HTTP Collection
This tool depends on [HTTP Toolkit](https://httptoolkit.tech/) to setup the HTTP(S) interception, which it hooks into the GraphQL over Websocket interface it exposes.

To get started:
 - Install and run [HTTP Toolkit](https://httptoolkit.tech/)
 - Point a device with the HTTP toolkit certificate installed towards the interception server
 - Edit `fingerprints/` modules:
   - Update the `fingerprints` dictionary, where keys are the types of data, and the values are the keys the program should look for
   - Update `MINIMUM_FINGERPRINTS` if needed, this is the minimum number of keys found to mark the input data as a hit
 - Edit `main.py`:
   - Add your `SOLR_HOST` (see [this](https://solr.apache.org/) if you are unfamiliar), `TARGET_HOSTNAME` (the hostname if the API you would like to collect data from)
 - Start `main.py`
   - If needed, print out `foundItem`s to update your database schema


## Note:
The contents of this repository are a personal project and in no way reflect work done for my employer.
