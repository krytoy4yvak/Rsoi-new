from mag import app
from flask_restful import Resource, abort, reqparse
from mag.repository.mag_repository import MagRepository
import jsonpickle
import flask
import json


def abort_if_mag_doesnt_exist(mag_id, repo):
    if not repo.exists(mag_id):
        app.logger.error('агазина с идентификатором %s не существует!', mag_id)
        abort(404, message="Mag {} doesn't exist".format(mag_id))


class MagResource(Resource):
    def get(self, mag_id):
        repo = MagRepository()
        app.logger.info('Получен запрос на получение информации о магазине с идентификатором %s' % mag_id)
        abort_if_mag_doesnt_exist(mag_id, repo)
        mag = repo.get(mag_id)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = mag.to_json() 
        app.logger.info('Запрос на получение информации о магазине с идентификатором %s успешно обработан' % mag_id)
        return response

    def delete(self, mag_id):
        repo = MagRepository()
        app.logger.info('Получен запрос на удаление витрины в магазине с идентификатором %s' % mag_id)
        abort_if_mag_doesnt_exist(mag_id, repo)
        repo.delete(mag_id)
        response = app.make_response("Mag %s deleted successfully" % mag_id)
        response.status_code = 204
        app.logger.info('Витрина в магазине с идентификатором %s успешно удален' % mag_id)
        return response

    def patch(self, mag_id):
        repo = MagRepository()
        app.logger.info('Получен запрос на покупку/возврат товара на полку в магазине с идентификатором %s' % mag_id)
        abort_if_mag_doesnt_exist(mag_id, repo)
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'status': 'buy', 'cell': 1}
        if payload["status"] == "buy":
            app.logger.info('Покупка товара')
            res = repo.get_a_seat(mag_id, payload["cell"])
            if res:
                response = app.make_response("")
                response.content_type = "application/json"
                response.status_code = 201
                app.logger.info('Успешно %s успешно куплено' % mag_id)
            else:
                response = app.make_response("This mag cannot be bought!")
                response.content_type = "application/json"
                response.status_code = 409
                app.logger.warning('Выбранное место на полке %s занято'
                                   % mag_id)
        else:
            app.logger.info('Возврат товара')
            res = repo.free_a_seat(mag_id, payload["cell"])
            if res:
                response = app.make_response("")
                response.content_type = "application/json"
                response.status_code = 201
                app.logger.info('Возврат товар в магазин %s успешно завершен' % mag_id)
            else:
                response = app.make_response("This mag cannot be released!")
                response.content_type = "application/json"
                response.status_code = 409
                app.logger.warning('Возврат товара в магазин %s не может быть завершен'
                                % mag_id)

        mag = repo.get(mag_id)
        response.data = mag.to_json()
        return response


class MagCreateResource(Resource):
    def post(self):
        repo = MagRepository()
        app.logger.info('Получен запрос на создание витрины')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'kassir_id': '5bd89b59af13c757e1b7f3fd', 'datetime': '12.11.2018_20:00', 'number_of_seats': 50}
        mag_id = repo.create(payload["kassir_id"], payload["datetime"], payload["number_of_seats"])
        mag = repo.get(mag_id)
        response = app.make_response("")
        response.status_code = 201
        response.content_type = "application/json"
        response.data = mag.to_json()
        app.logger.info('Витрина в магазине с идентификатором %s успешно создана' % mag_id)
        return response


class MagListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        repo = MagRepository()
        app.logger.info('Получен запрос на получение списка магазинов')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество магазинов на странице: %d' % (args['page'], args['page_size']))
        mags_list, is_prev_page, is_next_page = repo.read_paginated(page_number=args['page'],
                                                                       page_size=args['page_size'])
        mags = ''
        for mag in mags_list:
            mags += mag.to_json() + '\n'
        dictr = {"is_prev_page": is_prev_page, "is_next_page": is_next_page}
        mags += "\n" + json.dumps(dictr)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = mags
        app.logger.info('Запрос на получение списка магазинов успешно обработан')
        return response
