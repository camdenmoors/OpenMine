import threading
import json
from modules.example.start import LoadGenerationModule

config = json.load(open('../../config.json', 'r'))
modules = [LoadGenerationModule]
threads = []

for module in modules:
    thread = module(config)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()