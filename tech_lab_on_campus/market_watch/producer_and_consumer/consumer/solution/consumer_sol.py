from consumer_interface import mqConsumerInterface
from queue import Queue
import pika
import sys
import os

class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key, exchange_name, queue_name):
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        # self.channel = None
        self.setupRMQConnection()
    
    
    def setupRMQConnection(self):
        print("Setting up RMQ Connection")

        #set up connnection and channel
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()

        # Declare the topic exchange
        self.channel.queue_declare(queue='my_queue')
        self.channel.exchange_declare(
            exchange='my_exchange', 
            # routing_key='routing_key', 
        )
    
        # bind binding key
        self.channel.queue_bind(
            queue='my_queue',
            routing_key='routing_key',
            exchange='my_exchange',
        )
        
        #setup callback function
        self.channel.basic_consume(
            'my_queue', 
            self.onMessageCallback, 
            auto_ack=False
        )

    def onMessageCallback(self, channel, method, properties, body):
        print(body)
    
    def startConsuming(self):
        self.channel.start_consuming()
    
    def Del(self):
        self.channel.close()
        self.connection.close()
