from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_get_paginated_user, do_get_user, do_authorization, do_logout, do_get_code, do_get_auth_token
import json

mod = Blueprint('users', __name__)


@mod.route('/users/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    return render_template("/users/index.html")


@mod.route('/APIlogin1')
def APIlogin1():
    client_id = 1
    client_secret = 123
    result = do_get_code(client_id)
    if result.success:
        if result.response.status_code == 201:
            code_d = json.loads(result.response.content)
            code = code_d['code']
            response = redirect(url_for('users.APIlogin2', code=code, client_id=client_id, client_secret=client_secret))
            return response
        else:
            flash(result.response.content.decode('utf-8'), 'error')
            return redirect(url_for('users.login'))
    else:
        flash(result.error)
    return redirect(url_for('users.login'))


@mod.route('/APIlogin2')
def APIlogin2():
    client_id = request.args.get('client_id', type=int)
    client_secret = request.args.get('client_secret', type=int)
    code = request.args.get('code', type=str)
    result = do_get_auth_token(client_id, client_secret, code)
    if result.success:
        if result.response.status_code == 200:
            response = redirect(url_for('menu.index'))
            response.headers["Set-Cookie"] = result.response.headers["Set-Cookie"]
            g.user = result.response.cookies
            return response
        else:
            flash(result.response.content.decode('utf-8'))
            return redirect(url_for('users.login'))
    else:
        flash(result.error)
    return redirect(url_for('users.login'))


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("/users/login.html")
    else:
        fail = False
        if 'name' not in request.form or request.form['name'] == '':
            flash('Логин не задан', "error")
            fail = True
        if 'password' not in request.form or request.form['password'] == '':
            flash('Пароль не задан', "error")
            fail = True
        if fail:
            return redirect(url_for('users.login'))
        name = request.form['name']
        password = request.form['password']
        result = do_authorization(name, password)
        if result.success:
            if result.response.status_code == 200:
                response = redirect(url_for('menu.index'))
                response.headers["Set-Cookie"] = result.response.headers["Set-Cookie"]
                g.user = result.response.cookies
                #g.logged_in = True
                return response

            else:
                flash(result.response.content.decode('utf-8'))
                return redirect(url_for('users.login'))
        else:
            flash(result.error)
        return redirect(url_for('users.login'))


@mod.route('/users/logout')
def logout():
    result = do_logout()
    response = redirect(url_for(result.redirect))
    response.delete_cookie('token')
    return response


@mod.route('/users/get/<user_id>', methods=['GET', 'POST'])
def get(user_id):
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        result = do_get_user(user_id, request.cookies)
        if result.success:
            if result.response.status_code == 200:
                user = json.loads(result.response.content)
                prod_ids = user['prod_ids']
                return render_template("/users/get.html", user = user, prod_ids = prod_ids)
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash('Ошибка. Кассира или магазина не существует.', "error")
                return redirect(url_for('mags.get_all'), "error")
        else:
            flash(result.error, "error")
            return redirect(url_for('mags.get_all'))


@mod.route('/users/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('users.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_user(page, 10, request.cookies)
        if result.success:
            if result.response.status_code == 200:
                users_obj = result.response.content
                users_str = (str(users_obj)).split('\\n')
                n = len(users_str)
                users_str[0] = users_str[0][2:]
                users = []
                users_str[n-1] = users_str[n-1][0:-1]
                dictr = json.loads(users_str[n-1])
                users_str.remove(users_str[n-1])
                for user in users_str:
                    if user != "":
                        user1 = bytes(user, 'utf8')
                        users.append(json.loads(user1))
                return render_template("/users/get_all.html", users=users, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash("Потзователь не найден", "error")
                return redirect(url_for('users.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('users.index'))