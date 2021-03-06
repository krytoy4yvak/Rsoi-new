from kassir import app
from flask_restful import Resource, abort, reqparse
from kassir.repository.kassir_repository import KassirRepository
import jsonpickle
import flask
import json


def abort_if_kassir_doesnt_exist(kassir_id, repo):
    if not repo.exists(kassir_id):
        app.logger.error('Кассира с идентификатором %s не существует!', kassir_id)
        abort(404, message="Kassir {} doesn't exist".format(kassir_id))


class KassirResource(Resource):
    def get(self, kassir_id):
        repo = KassirRepository()
        app.logger.info('Получен запрос на получение информации о кассире с идентификатором %s' % kassir_id)
        abort_if_kassir_doesnt_exist(kassir_id, repo)
        kassir = repo.get(kassir_id)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = kassir.to_json()
        app.logger.info('Запрос на получение информации о кассире с идентификатором %s успешно обработан' % kassir_id)
        return response

    def delete(self, kassir_id):
        repo = KassirRepository()
        app.logger.info('Получен запрос на увольнение кассира с идентификатором %s' % kassir_id)
        abort_if_kassir_doesnt_exist(kassir_id, repo)
        repo.delete(kassir_id)
        response = app.make_response("Kassir %s deleted successfully" % kassir_id)
        response.status_code = 204
        app.logger.info('Кассир с идентификатором %s успешно уволен' % kassir_id)
        return response


class KassirCreateResource(Resource):
    def post(self):
        repo = KassirRepository()
        app.logger.info('Получен запрос по найму кассира')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'name': '1', 'stage': '2', 'year': 60}
        kassir_id = repo.create(payload["name"], payload["stage"], payload["year"])
        kassir = repo.get(kassir_id)
        response = app.make_response("")
        response.status_code = 201
        response.content_type = "application/json"
        response.data = kassir.to_json() #jsonpickle.encode(kassir)
        app.logger.info('Кассир с идентификатором %s успешно нанят' % kassir_id)
        return response


class KassirListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        repo = KassirRepository()
        app.logger.info('Получен запрос на получение списка кассиров')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество кассиров на странице: %d' % (args['page'], args['page_size']))
        kassirs_list, is_prev_page, is_next_page = repo.read_paginated(page_number=args['page'],
                                                                      page_size=args['page_size'])
        kassirs = ''
        for kassir in kassirs_list:
            kassirs += "\n" + kassir.to_json()
        dictr = {"is_prev_page": is_prev_page, "is_next_page": is_next_page}
        kassirs += "\n" + json.dumps(dictr)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = kassirs
        app.logger.info('Запрос на получение списка кассиров успешно обработан')
        return response
