from flask_restful import Api
from kassir.rest_api.kassir_resource import *



api = Api(app)
service_namespace = "/kassirs"

api.add_resource(KassirListResource, "/kassirs")
api.add_resource(KassirResource, "/kassirs/<kassir_id>")
api.add_resource(KassirCreateResource, "/kassirs/create")


if __name__ == '__main__':
    app.run(port=5001, debug=True)