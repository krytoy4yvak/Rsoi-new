import fl5.message_queue
import threading
import jsonpickle
import requests
from config import current_config
from gateway import app


class Request:
    def __init__(self, type, data):
        self.type = type
	    print(self.type)
        self.data = data
	    print(self.data)


class ProdReturnHandling(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queueee = fl5.message_queue.MessageQueue(["my_queue"], delay=5.0)
        self.queueee.bind("my_queue", "prod_return_handling_request")

    def run(self):
        while True:
            request_serialized = self.queueee.receive_message("my_queue")
            request = jsonpickle.decode(request_serialized)
            if request.type == "PROD_RETURN":
                try:
                    response = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                                              "/%s" % request.data["mag_id"], jsonpickle.encode(request.data["payload"]))
                    if response.status_code == 201:
                        app.logger.info('Освобождение места успешно завершено')
                    print(response)
                    else:
                        app.logger.warning('Освобождение места не может быть завершено')
                        self.queueee.send_message(request_serialized, "prod_return_handling_request")
                        print(self.queueee.send_message(request_serialized, "prod_return_handling_request"))
                except:
                    app.logger.warning(
                        'Освобождение места не может быть завершено, добавление запроса в очередь')
                    self.queueee.send_message(request_serialized, "prod_return_handling_request")
                    print(self.queueee.send_message(request_serialized, "prod_return_handling_request"))

