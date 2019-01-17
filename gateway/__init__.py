from flask import Flask
import commonnn.message_queue


app = Flask(__name__)
replay_request_queue = commonnn.message_queue.MessageQueue()