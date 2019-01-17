from functools import wraps
from flask import g, url_for, flash, abort, request, redirect, make_response
import requests
import requests.exceptions
from gui.config import current_config
import jsonpickle


class Result:
    def __init__(self, success, response=None, error=None, redirect=None):
        self.success = success
        self.error = error
        self.redirect = redirect
        self.response = response


def request_handler(redirect_url):
    def wrap(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                request_result = f(*args, **kwargs)
                return Result(success=True, redirect=redirect_url, response=request_result)
            except requests.exceptions.Timeout as e:
                return Result(success=False, error='Время ожидания ответа превышено. Повторите запрос позже')
            except requests.exceptions.ConnectionError as e:
                return Result(success=False, error='В данный момент сервис недоступен. Повторите запрос позже')
            except requests.exceptions.RequestException as e:
                return Result(success=False, error='Произошла ошибка. Повторите запрос позже')
        return decorated_function
    return wrap


@request_handler(redirect_url='prods.index')
def do_get_paginated_prods(page, page_size, cookies):
    result = gateway_api_request(current_config.PROD_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)), cookies=cookies)
    return result


@request_handler(redirect_url='users.login')
def do_get_code(client_id):
    result = gateway_api_request(current_config.USER_SERVICE_PATH+"/auth", 'POST',
                                 data={'client_id': client_id})
    return result


@request_handler(redirect_url='users.login')
def do_get_auth_token(client_id, client_secret, code):
    result = gateway_api_request(current_config.USER_SERVICE_PATH+"/auth", 'GET',
                                 data={'client_id': client_id, 'client_secret': client_secret, 'code': code})
    return result


@request_handler(redirect_url='prods.index')
def do_get_prod(prod_id, cookies):
    result = gateway_api_request(current_config.PROD_SERVICE_PATH+'/'+prod_id, 'GET', cookies=cookies)
    return result


@request_handler(redirect_url='prods.index')
def do_buy_prod(mag_id, seat_number, cookies):
    result = gateway_api_request(current_config.PROD_SERVICE_PATH+'/buy', 'POST', {'seat_number':seat_number,
                                                                                     'mag_id':mag_id},
                                 cookies=cookies)
    return result


@request_handler(redirect_url='prods.index')
def do_return_prod(prod_id, cookies):
    result = gateway_api_request(current_config.PROD_SERVICE_PATH+'/return/'+prod_id, 'DELETE', cookies=cookies)
    return result


@request_handler(redirect_url='mag.index')
def do_get_paginated_user(page, page_size, cookies):
    result = gateway_api_request(current_config.USER_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)), cookies=cookies)
    return result


@request_handler(redirect_url='user.login')
def do_authorization(login, password):
    result = gateway_api_request(current_config.USER_SERVICE_PATH+current_config.GET_TOKEN_URL_PATH, 'GET',
                                 params=(('name', login), ('password', password)))
    return result


@request_handler(redirect_url='menu.index')
def do_logout():
    response = make_response("")
    if 'token' in request.cookies:
        response.delete_cookie('token')
    return response


@request_handler(redirect_url='mag.index')
def do_get_user(user_id, cookies):
    result = gateway_api_request(current_config.USER_SERVICE_PATH+'/'+user_id, 'GET', cookies=cookies)
    return result


@request_handler(redirect_url='kassirs.get_all')
def do_create_mag(kassir_id, number_of_seats, date_time, cookies):
    result = gateway_api_request(current_config.MAG_SERVICE_PATH + current_config.CREATE_PATH, 'POST',
                                 {'kassir_id': kassir_id,
                                  'datetime': date_time,
                                  'number_of_seats': int(number_of_seats)}, cookies=cookies)
    return result


@request_handler(redirect_url='mag.index')
def do_get_paginated_mag(page, page_size, cookies):
    result = gateway_api_request(current_config.MAG_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)), cookies=cookies)
    return result


@request_handler(redirect_url='mag.index')
def do_get_mag(mag_id, cookies):
    result = gateway_api_request(current_config.MAG_SERVICE_PATH+'/'+mag_id, 'GET', cookies=cookies)
    return result


@request_handler(redirect_url='kassirs.index')
def do_create_kassir(name, stage, year, cookies):
    result = gateway_api_request(current_config.KASSIR_SERVICE_PATH + current_config.CREATE_PATH, 'POST',
                                 {'name': name, 'stage': stage, 'year': int(year)}, cookies=cookies)
    return result


@request_handler(redirect_url='kassirs.index')
def do_get_kassir(kassir_id, cookies):
    result = gateway_api_request(current_config.KASSIR_SERVICE_PATH + '/' + kassir_id, 'GET', cookies=cookies)
    return result


@request_handler(redirect_url='kassirs.index')
def do_get_paginated_kassir(page, page_size, cookies):
    result = gateway_api_request(current_config.KASSIR_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)), cookies=cookies)
    return result


@request_handler(redirect_url='kassirs.index')
def do_delete_kassir(kassir_id, cookies):
    result = gateway_api_request(current_config.KASSIR_SERVICE_PATH + '/' + kassir_id, 'DELETE', cookies)
    return result


def gateway_api_request(service_path, method, data=None, params=None, cookies=None):
    tmp = service_path
    if method == 'GET':
        return requests.get(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                            + service_path, data=jsonpickle.encode(data), params=params, cookies=cookies)
    elif method == 'POST':
        return requests.post(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                             + service_path, data=jsonpickle.encode(data), params=params,
                             cookies=cookies)
    elif method == 'PUT':
        return requests.put(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                            + service_path, data, params=params, cookies=cookies)
    elif method == 'DELETE':
        return requests.delete(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                               + service_path, cookies=cookies)
    elif method == 'PATCH':
        return requests.patch(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                              + service_path, data, cookies=cookies)
    else:
        abort(400)