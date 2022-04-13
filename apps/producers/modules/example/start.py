from threading import Thread
import json
import pika
import time

class LoadGenerationModule(Thread):
    config: dict
    connection: pika.BlockingConnection

    def __init__(self, config: dict):
        Thread.__init__(self)
        self.config = config
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(config['amqp']['host']))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=config['amqp']['queue'])
    
    def sendMessage(self, message: dict):
        self.channel.basic_publish(exchange="", routing_key=self.config['amqp']['queue'], body=json)

    def run(self):
        while True:
            print("[x] Sent 'Hello World!'")
            time.sleep(1)

if __name__ == "__main__":
    print("This is a module.")