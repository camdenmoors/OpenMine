import time
from modules.base import BaseProducerClass

class LoadGenerationModule(BaseProducerClass):
    def run(self):
        while True:
            self.sendMessage({'source': self.threadId})
            time.sleep(1)

if __name__ == "__main__":
    print("This is a module.")