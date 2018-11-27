from prod import app
from flask_restful import Resource, abort, reqparse
from prod.repository.prod_repository import ProdRepository
import jsonpickle
import flask


repo = ProdRepository()


def abort_if_mag_doesnt_exist(prod_id):
    if not repo.exists(prod_id):
        app.logger.error('Билета с идентификатором %s не существует!', prod_id)
        abort(404, message="Prod {} doesn't exist".format(prod_id))


class ProdResource(Resource):
    def get(self, prod_id):
        app.logger.info('Получен запрос на получение информации о билете с идентификатором %s' % prod_id)
        abort_if_mag_doesnt_exist(prod_id)
        prod = repo.get(prod_id)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = prod.to_json()
        app.logger.info('Запрос на получение информации о билете с идентификатором %s успешно обработан'
                        % prod_id)
        return response

    def delete(self, prod_id):
        app.logger.info('Получен запрос на удаление билета с идентификатором %s' % prod_id)
        abort_if_mag_doesnt_exist(prod_id)
        repo.delete(prod_id)
        response = app.make_response("Prod %s deleted successfully" % prod_id)
        response.status_code = 204
        app.logger.info('Билет с идентификатором %s успешно удален' % prod_id)
        return response


class ProdCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание (покупку) билета')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {"mag_id": "5bd897f8af13c78fe908cb98", "prod_col": 1}
        prod_id = repo.create(payload["mag_id"], payload["prod_col"])
        prod = repo.get(prod_id)
        response = app.make_response("")
        response.content_type = "application/json"
        response.status_code = 201
        response.data = prod.to_json()
        app.logger.info('Бмлет с идентификатором %s успешно создан (куплен)' % prod_id)
        return response


class ProdListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        app.logger.info('Получен запрос на получение списка билетов')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество билетов на странице: %d' % (args['page'], args['page_size']))
        prod_list = repo.read_paginated(page_number=args['page'], page_size=args['page_size'])
        prods = ''
        for prod in prod_list:
            prods += prod.to_json() + '\n'
        response = app.make_response("")
        response.content_type = "application/json"
        response.status_code = 200
        response.data = prods
        app.logger.info('Запрос на получение списка билетов успешно обработан')
        return response
