import flask
import jsonpickle
import requests
from flask_restful import Resource, reqparse
from mag.domain.mag import Mag
from kassir.domain.kassir import Kassir
from prod.domain.prod import Prod
from user.domain.user import User
from config import current_config
from gateway import app
import json
from flask import Flask, render_template




class GatewayProdResource(Resource):



    def get(self, prod_id):
        app.logger.info('Получен запрос на получение информации о товаре с идентификатором %s' % prod_id)
        response = requests.get(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH + "/%s" % prod_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
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
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество билетов на странице: %d' % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        paybuy = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH, params=paybuy)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка товаров успешно обработан')
        else:
            app.logger.warning('Список товаров не может быть получен')
        return result


class GatewayMagResource(Resource):
    def get(self, mag_id):
        app.logger.info('Получен запрос на получение подробной информации о магазине с идентификатором %s' % mag_id)
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

        mag = Mag.from_json(response_mag.content) #jsonpickle.decode(response_mag.content)
        kassir_id = str(mag.kassir_id)

        response_kassir = requests.get(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                                      "/%s" % kassir_id)
        if response_kassir.status_code == 200:
            app.logger.info('Запрос на получение информации о кассире с идентификатором %s успешно обработан'
                            % kassir_id)
        else:
            app.logger.warning('Информация о кассире с идентификатором %s не модет быть получена' % kassir_id)
            result = flask.Response(status=response_kassir.status_code, headers=response_kassir.headers.items(),
                                    response=response_kassir.content)
            return result
        kassir = kassir.from_json(response_kassir.content)
        response = mag.to_json() + '\n' + kassir.to_json()
        result = flask.Response(status=response_mag.status_code, headers=response_mag.headers.items(),
                                response=response)
        app.logger.info('Запрос на получение подробной информации о касире с идентификатором %s успешно обработан'
                        % mag_id)
        return result


class GatewayMagCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание магазина')
        try:
            response = requests.post(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
        except:
            paybuy = {'kassir_id': '5bd89b59af13c757e1b7f3fd', 'datetime': '12.11.2018_20:00', 'number_of_col': 50}
            response = requests.post(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                                     current_config.CREATE_PATH, data = jsonpickle.encode(paybuy))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Магазин успешно создан')
        else:
            app.logger.warning('Магазин не может быть создан')
        return result


class GatewayMagListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка магазинов')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество сеансов на странице: %d' % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        paybuy = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH, params=paybuy)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка магазнов успешно обработан')
        else:
            app.logger.warning('Список магазинов не может быть получен')
        return result


class GatewayKassirResource(Resource):
    def get(self, kassir_id):
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
        app.logger.info('Получен запрос на создание кассира')
        try:
            response = requests.post(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
        except:
            paybuy = {'name': 'test', 'razryad': 'test', 'year': 30}
            response = requests.post(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=jsonpickle.encode(paybuy))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Касир успешно создан')
        else:
            app.logger.warning('Кассир не может быть создан')
        return result


class GatewayKassirListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка кассиров')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        page = args['page']
        page_size = args['page_size']
        app.logger.info('Номер страницы: %d; количество фильмов на странице: %d' % (args['page'], args['page_size']))
        paybuy = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH, params=paybuy)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка кассиров успешно обработан')
        else:
            app.logger.warning('Список кассиров не может быть получен')
        return result


class GatewayUserResource(Resource):
    def get(self, user_id):
        app.logger.info('Получен запрос на получение информации о пользователе с идентификатором %s' % user_id)
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
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество пользователей на странице: %d'
                        % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        paybuy = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH, params=paybuy)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка пользователей успешно обработан')
        else:
            app.logger.warning('Список пользователей не может быть получен')
        return result


class GatewayBuyProd(Resource):
    user_id = "5bfcead1102bd227a40adf03"

    def post(self):
        app.logger.info('Получен запрос на покупку товара')
        paybuy = jsonpickle.decode(flask.request.data)
        paybuy1 = {'prod_col': paybuy["prod_col"], 'status': 'buy'}
        response = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH + "/%s" % paybuy["mag_id"], jsonpickle.encode(paybuy1))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 201:
            app.logger.error('Покупка товара в магазине с идентификатором %s не может быть выполнена'
                             % paybuy["mag_id"])
            return result
        else:
            app.logger.info('Касса магазина с идентификатором %s для пользователя с идентификатором %s успешно открыта'
                            % (paybuy["mag_id"], self.user_id))

        response = requests.post(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                                 current_config.CREATE_PATH, jsonpickle.encode(paybuy))
        prod = Prod.from_json(response.content) #jsonpickle.decode(response.content)
        if response.status_code == 201:
            app.logger.info('Товар с идентификатором %s успешно создан' % str(prod.id))
        else:
            paybuy1['status'] = 'return'
            requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH + "/" +
                           paybuy["mag_id"], jsonpickle.encode(paybuy1))
            app.logger.warning('Товар не может быть создан')
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)

        paybuy3 = {'prod_id': str(prod.id), 'status': 'buy'}
        response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                  "/%s" % self.user_id, jsonpickle.encode(paybuy3))
        if response.status_code == 201:
            app.logger.info('Покупка товара для пользователя успешно произведена')
        else:
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            paybuy1['status'] = 'return'
            requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH + "/" +
                           paybuy["mag_id"], jsonpickle.encode(paybuy1))
            requests.delete(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH + "/" +
                            paybuy3['prod_id'])
            app.logger.warning('Покупка товара не может быть завершена')
        return result


class GatewayReturnProd(Resource):
    user_id = "5bfcead1102bd227a40adf03"

    def delete(self, prod_id):
        app.logger.info('Получен запрос на возврат товара')
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

        prod = Prod.from_json(response.content) #jsonpickle.decode(response.content)
        paybuy1 = {'prod_col': prod.prod_col, 'status': 'return'}
        response = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH + "/%s" % prod.mag_id, jsonpickle.encode(paybuy1))
        if response.status_code == 201:
            app.logger.info('Освобождение места в магазине завершен')
        else:
            app.logger.warning('Освобождение места в магазине не может быть завершено')
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        paybuy3 = {'prod_id': prod_id, 'status': 'return'}
        response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH + "/%s" % self.user_id, jsonpickle.encode(paybuy3))
        if response.status_code == 201:
            app.logger.info('Возврат товара для пользователя %s успешно произведен' % self.user_id)
        else:
            paybuy1['status'] = 'buy'
            requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                           "/%s" % prod.mag_id, jsonpickle.encode(paybuy1))
            app.logger.warning('Возврат товра для пользователя %s не может быть произведен' % self.user_id)
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        response = requests.delete(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                                   "/%s" % prod_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 204:
            app.logger.info('ТОвар с идентификатором %s успешно удален' % prod_id)
        else:
            paybuy1['status'] = 'buy'
            requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                           "/%s" % prod.mag_id, jsonpickle.encode(paybuy1))
            paybuy3['status'] = 'buy'
            requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/%s" % self.user_id, jsonpickle.encode(paybuy3))
            app.logger.warning('Товар с идентификатором %s не может быть удален' % prod_id)
        return result
