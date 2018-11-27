from kassir import app
from flask_restful import Api
from gateway.rest_api.gateway_api import *
from flask import Flask, render_template

api = Api(app)

api.add_resource(GatewayBuyProd, "/gateway/api/prods/buy")
api.add_resource(GatewayReturnProd, "/gateway/api/prods/return" + "/<prod_id>")
api.add_resource(GatewayProdResource, "/gateway/api/prods" + "/<prod_id>")
api.add_resource(GatewayProdListResource, "/gateway/api/prods")
api.add_resource(GatewayMagResource, "/gateway/api/mags" + "/<mag_id>")
api.add_resource(GatewayMagListResource, "/gateway/api/mags")
api.add_resource(GatewayMagCreateResource, "/gateway/api/mags/create")
api.add_resource(GatewayKassirResource, "/gateway/api/kassirss" + "/<kassir_id>")
api.add_resource(GatewayKassirListResource, "/gateway/api/kassirs")
api.add_resource(GatewayKassirCreateResource, "/gateway/api/kassirs/create")
api.add_resource(GatewayUserResource, "/gateway/api/users" + "/<user_id>")
api.add_resource(GatewayUserListResource, "/gateway/api/users")


if __name__ == '__main__':
    app.run(debug=True)