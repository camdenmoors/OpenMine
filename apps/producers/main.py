import uuid
import json
from modules.example.start import LoadGenerationModule
from modules.https.start import HTTPSInterceptionModule

config = json.load(open('../../config.json', 'r'))
modules = [
    #LoadGenerationModule,
    HTTPSInterceptionModule
]
threads = []

for module in modules:
    thread = module(config, str(uuid.uuid4()))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()