from prod import app
from flask_restful import Api
from prod.rest_api.prod_resource import *
from prod.repository.prod_repository import Prods


api = Api(app)
service_namespace = "/prods"

api.add_resource(ProdListResource, "/prods")
api.add_resource(ProdResource, "/prods/<prod_id>")
api.add_resource(ProdCreateResource, "/prods/create")


if __name__ == '__main__':
    app.run(port=5003, debug=True)