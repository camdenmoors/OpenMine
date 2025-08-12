import uuid
import json
import os
import signal
import sys
from modules.example.start import LoadGenerationModule
from modules.https.start import HTTPSInterceptionModule

base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, '..', '..', 'config.json')
config = json.load(open(config_path, 'r'))

modules = [
    #LoadGenerationModule,
    HTTPSInterceptionModule
]

threads = []

def shutdown_handler(sig, frame):
    print("\nCtrl+C detected. Shutting down...")
    for thread in threads:
        if hasattr(thread, "stop"):
            thread.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)

for module in modules:
    thread = module(config, str(uuid.uuid4()))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
