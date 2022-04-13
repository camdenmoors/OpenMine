from threading import Thread
from event import Event
import pika
import logging

logging.getLogger("pika").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class BaseProducerClass(Thread):
    config: dict
    threadId: str
    connection: pika.BlockingConnection

    def log(self, message: str):
        logging.info(f"{self.threadId}: {message}")
    
    def debug(self, message: str):
        logging.debug(f"{self.threadId}: {message}")

    def sendEvent(self, event: Event):
        messageStr = event.to_dict()
        self.debug(f"MSG: {messageStr}")
        try:
            self.channel.basic_publish(exchange="", routing_key=self.config['amqp']['queue'], body=messageStr)
        except Exception as e:
            self.log('Error sending message')
            print(e)    

    def __init__(self, config: dict, threadId: str):
        Thread.__init__(self)
        self.threadId = threadId
        self.log(f"New thread for {self.__class__.__name__}")
        self.config = config
        self.log(f"Creating AMQP Connection to host {config['amqp']['host']}")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(config['amqp']['host'], heartbeat=600))
        self.log(f"Connected to host {config['amqp']['host']}")
        self.log(f"Creating message channel")
        self.channel = self.connection.channel()
        self.log(f"Created message channel")
        self.log(f"Declaring message queue {config['amqp']['queue']}")
        self.channel.queue_declare(queue=config['amqp']['queue'])