from user import app
from flask_restful import Resource, abort, reqparse
from user.repository.user_repository import UserRepository
import jsonpickle
import flask


repo = UserRepository()


def abort_if_user_doesnt_exist(user_id):
    if not repo.exists(user_id):
        app.logger.error('Пользователя с идентификатором %s не существует!', user_id)
        abort(404, message="User {} doesn't exist".format(user_id))


class UserResource(Resource):
    def get(self, user_id):
        app.logger.info('Получен запрос на получение информации о пользователе с идентификатором %s' % user_id)
        abort_if_user_doesnt_exist(user_id)
        user = repo.get(user_id)
        response = app.make_response("")
        response.status_code = 200
        response.data = user.to_json()
        response.content_type = "application/json"
        app.logger.info('Запрос на получение информации о пользователе с идентификатором %s успешно обработан'
                        % user_id)
        return response

    def delete(self, user_id):
        app.logger.info('Получен запрос на удаление пользователя с идентификатором %s' % user_id)
        abort_if_user_doesnt_exist(user_id)
        repo.delete(user_id)
        response = app.make_response("User %s deleted successfully" % user_id)
        response.status_code = 204
        app.logger.info('Пользователь с идентификатором %s успешно удален' % user_id)
        return response

    def patch(self, user_id):
        app.logger.info('Получен запрос на покупку/возврат товара для пользователя с идентификатором %s' % user_id)
        abort_if_user_doesnt_exist(user_id)
        payload = jsonpickle.decode(flask.request.data)
        if payload["status"] == "buy":
            app.logger.info('Покупка товара с идентификатором %s' % payload["prod_id"])
            repo.assign_prod(user_id, payload["prod_id"])
        else:
            app.logger.info('Возврат товара с идентификатором %s' % payload["prod_id"])
            repo.remove_prod(user_id, payload["prod_id"])
        user = repo.get(user_id)
        response = app.make_response("")
        response.status_code = 201
        response.data = user.to_json()
        response.content_type = "application/json"
        if payload["status"] == "buy":
            app.logger.info('Покупка товара %s для пользователя %s успешно произведена'
                            % (payload["prod_id"], user_id))
        else:
            app.logger.info('Возврат товара %s для пользователя %s успешно произведен'
                            % (payload["prod_id"], user_id))
        return response


class UserCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание пользователя')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'l_name': 'test', 'p_name': 'test'}
        user_id = repo.create(payload["l_name"], payload["p_name"])
        user = repo.get(user_id)
        response = app.make_response("")
        response.status_code = 201
        response.data = user.to_json()
        response.content_type = "application/json"
        app.logger.info('Запрос на создание нового пользователя успешно обработан, идентификатор: %s' % user_id)
        return response


class UserListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        app.logger.info('Получен запрос на получение списка пользователей')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество пользователей на странице: %d' % (args['page'], args['page_size']))
        users_list = repo.read_paginated(page_number=args['page'], page_size=args['page_size'])
        users = ''
        for user in users_list:
            users += user.to_json() + '\n'
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = users
        app.logger.info('Запрос на получение списка пользователей успешно обработан')
        return response
