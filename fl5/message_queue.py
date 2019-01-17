import pika
import logging
import time

class MessageQueue:
    EXCHANGE_NAME = "rra-direct"
    #RABBIT_HOST_IP="127.0.0.1"

    def __init__(self, queue_names = None, host="localhost", delay=5.0):
        self.delay = delay
	    print(self.delay)
        self.logger = logging.getLogger(self.__class__.__name__)
	    print(self.logger )
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( ))
	    print(self.connection)
        self.queues = {}
        self.channel = self.connection.channel()
	    print(self.channel)
        self.channel.exchange_declare(exchange=self.EXCHANGE_NAME,
                                      exchange_type="direct")
        if queue_names is not None:
            for queue_name in queue_names:
                self.add_queue(queue_name)
			print(self.add_queue)

    def send_message(self, message, routing_key):
        self.channel.basic_publish(exchange=self.EXCHANGE_NAME,
                                   routing_key=routing_key,
                                   body=message)
	   print(channel.basic_publish)
        self.logger.debug("Message : %s sent" % message)

    def receive_message(self, queue_name):
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)
print(channel.basic_get)

        while method_frame is None or method_frame.NAME == 'Basic.GetEmpty':
            method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)
            time.sleep(self.delay)
print(self.channel.basic_get)


        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return body
print(self.channel.basic_ack)


    def bind(self, queue_name, routing_key):
        if queue_name in self.queues.keys():
            self.channel.queue_bind(exchange=self.EXCHANGE_NAME,
                                    queue=queue_name,
                                    routing_key=routing_key)
		 print(self.channel.queue_bind)
        else:
            self.logger.error("Queue %s not found" % queue_name)

    def add_queue(self, queue_name):
        if queue_name not in self.queues.keys():
            self.queues[queue_name] = self.channel.queue_declare(queue=queue_name)
print(self.channel.queue_declare)
        else:
            self.logger.error("Queue %s already exists" % queue_name)
print(self.logger.error)
