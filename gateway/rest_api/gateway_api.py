import flask
import jsonpickle
import requests
from flask_restful import Resource, reqparse
from mag.domain.mag import Mag
from kassir.domain.kassir import Kassir
from prod.domain.prod import Prod
from user.domain.user import User
from config import current_config
from gateway import app, replay_request_queue
from gateway.fl5.prod_return_handling import Request
import json


class GatewayProdResource(Resource):
    def get(self, prod_id):
        app.logger.info('Получен запрос на получение информации о товаре с идентификатором %s' % prod_id)
        req = requests.session()
        print(reg)
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']
        print(token)

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        print(response)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        print(result)
        if result.status_code != 200:
            return result
        response = requests.get(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                                "/%s" % prod_id)
        print(response)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        print(result)
        if response.status_code == 200:
            app.logger.info('Информация о товаре с идентификатором %s успещно получена' % prod_id)
        else:
            app.logger.warning('Информация о товаре с идентификатором %s не может быть получена' % prod_id)
        return result


class GatewayProdListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка товаров')
        try:
            args = self.parser.parse_args(strict=True)
            print(args)
            req = requests.session()
            print(reg)
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']
            print(token)

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            print(response)
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            print(result)
            if result.status_code != 200:
                return result
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество товаров на странице: %d' % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        print(payload)
        response = requests.get(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH, params=payload)
        print(response)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        print(result)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка билетов успешно обработан')
        else:
            app.logger.warning('Список билетов не может быть получен')
        return result


class GatewayMagResource(Resource):
    def get(self, mag_id):
        app.logger.info('Получен запрос на получение подробной информации о магазине с идентификатором %s' % mag_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        response_mag = requests.get(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                                       "/%s" % mag_id)
        if response_mag.status_code == 200:
            app.logger.info('Запрос на получение информации о магазине с идентификатором %s успешно обработан'
                            % mag_id)
        else:
            app.logger.warning('Информация о магазине с идентификатором %s не модет быть получена' % mag_id)
            result = flask.Response(status=response_mag.status_code, headers=response_mag.headers.items(),
                                    response=response_mag.content)
            return result

        mag = Mag.from_json(response_mag.content)
        kassir_id = str(mag.kassir_id)

        try:
            response_kassir = requests.get(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                                          "/%s" % kassir_id)
        except:
            response_kassir = None
        if response_kassir is not None and response_kassir.status_code == 200:
            app.logger.info('Запрос на получение информации о кассире с идентификатором %s успешно обработан'
                            % kassir_id)
            kassir = Kassir.from_json(response_kassir.content)
            response = mag.to_json() + '\n' + kassir.to_json()
        else:
            app.logger.warning('Информация о касире с идентификатором %s не модет быть получена' % kassir_id)
            kassir = {'kassir_id': 'Not available', 'name': 'Not available',
                     'stage': 'Not available', 'year': 'Not available'}
            response = mag.to_json() + '\n' + json.dumps(kassir)

        result = flask.Response(status=response_mag.status_code, headers=response_mag.headers.items(),
                                response=response)
        app.logger.info('Запрос на получение подробной информации о магазине с идентификатором %s успешно обработан'
                        % mag_id)
        return result

class GatewayMagCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание витрины')
        try:
            response = requests.post(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
            print(response)
            req = requests.session()
            print(reg)
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']
            print(token)

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            payload = {'kassir_id': '5bd89b59af13c757e1b7f3fd', 'datetime': '15.11.2018_00:00', 'number_of_seats': 50}
            print(payload)
            response = requests.post(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                                     current_config.CREATE_PATH, data = jsonpickle.encode(payload))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Витрина успешно создан')
        else:
            app.logger.warning('Витрина не может быть создан')
        return result


class GatewayMagListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка магазинов')
        try:
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество магазинов на странице: %d' % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка магазиов успешно обработан')
        else:
            app.logger.warning('Список магазинов не может быть получен')
        return result


class GatewayKassirResource(Resource):
    def get(self, kassir_id):
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        app.logger.info('Получен запрос на получение информации о кассире с идентификатором %s' % kassir_id)
        response = requests.get(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                                "/%s" % kassir_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о кассире с идентификатором %s успешно обработан' % kassir_id)
        else:
            app.logger.warning('Информация о кассире с идентификатором %s не может быть получена' % kassir_id)
        return result

    def delete(self, kassir_id):
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        app.logger.info('Получен запрос на увольнение кассира с идентификатором %s' % kassir_id)
        response = requests.delete(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                                   "/%s" % kassir_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 204:
            app.logger.info('Кассир с идентификатором %s успешно уволен' % kassir_id)
        else:
            app.logger.warning('Кассир с идентификатором %s не может быть уволен' % kassir_id)
        return result


class GatewayKassirCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на добавление кассира')
        try:
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
            response = requests.post(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
        except:
            payload = {'name': 'test', 'stage': 'test', 'year': 30}
            response = requests.post(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Кассир успешно добавлен')
        else:
            app.logger.warning('Кассир не может быть добавлен')
        return result


class GatewayKassirListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка работников')
        try:
            args = self.parser.parse_args(strict=True)
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            args = {'page': 1, 'page_size': 5}
        page = args['page']
        page_size = args['page_size']
        app.logger.info('Номер страницы: %d; количество работников на странице: %d' % (args['page'], args['page_size']))
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка работников успешно обработан')
        else:
            app.logger.warning('Список работников не может быть получен')
        return result


class GatewayUserResource(Resource):
    def get(self, user_id):
        app.logger.info('Получен запрос на получение информации о пользователе с идентификатором %s' % user_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о пользователе с идентификатором %s успешно обработан'
                            % user_id)
        else:
            app.logger.warning('Информация о пользователе с идентификатором %s не может быть получена' % user_id)
        return result


class GatewayUserListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка пользователей')
        try:
            args = self.parser.parse_args(strict=True)
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество пользователей на странице: %d'
                        % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка пользователей успешно обработан')
        else:
            app.logger.warning('Список пользователей не может быть получен')
        return result


class GatewayAuthorization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("password", type=str)

    def get(self):
        app.logger.info('Получен запрос на аутентификацию')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        args = self.parser.parse_args(strict=True)
        login = args['name']
        password = args['password']
        payload = {'name': login, 'password': password}
        response = req.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           current_config.GET_TOKEN_URL_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на авторизацию успешно обработан')
        else:
            app.logger.warning('Авторизация не может быть произведена')
        return result


class GatewayApiAuthorization(Resource):
    def post(self):
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        payload = jsonpickle.decode(flask.request.data)
        client_id = payload['client_id']
        response = req.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH + "/auth/token",
                            data=jsonpickle.encode({'client_id': client_id}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def get(self):
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        payload = jsonpickle.decode(flask.request.data)
        client_id = payload['client_id']
        client_secret = payload['client_secret']
        code = payload['code']
        response = req.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH + "/token",
                            data=jsonpickle.encode({'client_id': client_id, 'client_secret': client_secret,
                                                    'code': code}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayBuyProd(Resource):


    def post(self):
        app.logger.info('Получен запрос на покупку билета')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        user = User.from_json(response.content)
        user_id = user.id
        payload = jsonpickle.decode(flask.request.data)
        payload1 = {'cell': payload["cell"], 'status': 'buy'}
        response = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                                  "/%s" % payload["mag_id"], jsonpickle.encode(payload1))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 201:
            app.logger.error('Покупка товара в магазине с идентификатором %s не может быть выполнена'
                             % payload["mag_id"])
            return result
        else:
            app.logger.info('Пользователь %s взял товар с полки в магазине с идентификатором %s'
                            % (user_id, payload["mag_id"]))

        response = requests.post(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                                 current_config.CREATE_PATH, jsonpickle.encode(payload))
        prod = Prod.from_json(response.content)
        if response.status_code == 201:
            app.logger.info('Товра с идентификатором %s успешно создан' % str(prod.id))
        else:
            payload1['status'] = 'return'
            requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH + "/" +
                           payload["mag_id"], jsonpickle.encode(payload1))
            app.logger.warning('Товар не может быть создан')
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)

        payload3 = {'prod_id': str(prod.id), 'status': 'buy'}
        response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                  "/%s" % user_id, jsonpickle.encode(payload3))
        if response.status_code == 201:
            app.logger.info('Покупка товара для пользователя успешно произведена')
        else:
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            payload1['status'] = 'return'
            requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH + "/" +
                           payload["mag_id"], jsonpickle.encode(payload1))
            requests.delete(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH + "/" +
                            payload3['prod_id'])
            app.logger.warning('Покупка товара не может быть завершена')
        return result


class GatewayReturnProd(Resource):


    def delete(self, prod_id):
        app.logger.info('Получен запрос на возврат товара')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        user = User.from_json(response.content)
        user_id = user.id

        response = requests.get(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                                "/%s" % prod_id)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о товаре с идентификатором %s успешно обработан'
                            % prod_id)
        else:
            app.logger.warning('Информация о товаре с идентификатором %s не может быть получена' % prod_id)
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        prod = Prod.from_json(response.content)
        payload1 = {'cell': prod.cell, 'status': 'return'}
        try:
            response = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                                    "/%s" % prod.mag_id, jsonpickle.encode(payload1))
            if response.status_code == 201:
                app.logger.info('Освобождение места на витрине в магазине успешно завершен')
            else:
                app.logger.warning('Освобождение места на витрине в магазине не может быть завершено, добавляем запрос в очередь')
                replay_request_queue.send_message(
                    jsonpickle.encode(Request("PROD_RETURN", data={"mag_id": prod.mag_id,
                                                                    "payload": payload1})),
                    "prod_return_handling_request")
        except:
            app.logger.warning(
                'Освобождение места на витрине в магазине не может быть завершено, добавление запроса в очередь')
            replay_request_queue.send_message(jsonpickle.encode(Request("PROD_RETURN", data={"mag_id": prod.mag_id,
                                                                                               "payload": payload1})),
                                              "prod_return_handling_request")
        finally:

            payload3 = {'prod_id': prod_id, 'status': 'return'}
            response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                      "/%s" % user_id, jsonpickle.encode(payload3))
            if response.status_code == 201:
                app.logger.info('Возврат товара для пользователя %s успешно произведен' % user_id)
            else:
                payload1['status'] = 'buy'
                requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                               "/%s" % prod.mag_id, jsonpickle.encode(payload1))
                app.logger.warning('Возврат товара для пользователя %s не может быть произведен' % user_id)
                result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                        response=response.content)
                return result

            response = requests.delete(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                                       "/%s" % prod_id)
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if response.status_code == 204:
                app.logger.info('Товар с идентификатором %s успешно удален' % prod_id)
            else:
                payload1['status'] = 'buy'
                requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                               "/%s" % prod.mag_id, jsonpickle.encode(payload1))
                payload3['status'] = 'buy'
                requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                               "/%s" % user_id, jsonpickle.encode(payload3))
                app.logger.warning('Товар с идентификатором %s не может быть удален' % prod_id)
            return result
