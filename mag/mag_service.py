
from flask_restful import Api
from mag.rest_api.mag_resource import *



api = Api(app)
service_namespace = "/mags"

api.add_resource(MagListResource, "/mags")
api.add_resource(MagResource, "/mags/<mag_id>")
api.add_resource(MagCreateResource, "/mags/create")


if __name__ == '__main__':
    app.run(port=5002, debug=True)