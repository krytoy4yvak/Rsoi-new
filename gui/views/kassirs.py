from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, Markup
from gui.utils import do_create_kassir, do_get_kassir, do_delete_kassir, do_get_paginated_kassir, do_logout
import json

mod = Blueprint('kassirs', __name__)


@mod.route('/kassirs/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    return render_template("/kassirs/index.html")


@mod.route('/kassirs/create', methods=['GET', 'POST'])
def create():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        return render_template("/kassirs/create.html")
    else:
        failed = False
        if 'name' not in request.form or request.form['name']=='':
            flash('Имя не задано', "error")
            failed = True

        if 'stage' not in request.form or request.form['stage']=='':
            flash('Ранг не задан', "error")
            failed = True

        if 'year' not in request.form or request.form['year']=='':
            flash('Стаж не задана', "error")
            failed = True

        if failed:
            return redirect(url_for('kassirs.create'))

        name = request.form['name']
        stage = request.form['stage']
        year = int(request.form['year'])
        if not isinstance(year, int):
            flash('Error', 'error')
            return redirect(url_for('kassirs/create'))
        result = do_create_kassir(name, stage, year, request.cookies)
        if result.success:
            if result.response.status_code == 201:
                flash('Кассир успешно добавлен', "info")
                response = redirect('kassirs/create')
                return response
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash(result.response.content.decode('utf-8'), "error")
                return redirect(url_for('kassirs.create'))
        else:
            flash(result.error)
            return redirect(url_for('kassirs/create'), "error")


@mod.route('/kassirs/get', methods=['GET', 'POST'])
def get():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        return render_template("/kassirs/get.html", kassir_found = False)
    else:
        if 'kassir_id' not in request.form or request.form['kassir_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('kassirs.get'))
        else:
            kassir_id = request.form["kassir_id"]
            result = do_get_kassir(kassir_id, request.cookies)

            if result.success:
                if result.response.status_code == 200:
                    kassir = json.loads(result.response.content)
                    return render_template("/kassirs/get.html", kassir=kassir, kassir_found=True)
                elif result.response.status_code == 403:
                    do_logout()
                    return redirect(url_for('users.login'))
                else:
                    flash("Кассир не найден", "error")
                    return redirect(url_for('kassirs.get'))
            else:
                flash(result.error, "error")
                return redirect(url_for('kassirs.get'))


@mod.route('/kassirs/delete/<kassir_id>', methods=['GET', 'POST'])
def delete(kassir_id):
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        return render_template("/kassirs/delete.html", kassir_id=kassir_id)
    else:
        if request.form['submit'] == 'Нет':
            return redirect(url_for('kassirs.get_all'))
        if request.form['submit'] == 'Да':
            #kassir_id = request.args["kassir_id"]
            result = do_delete_kassir(kassir_id, request.cookies)

            if result.success:
                if result.response.status_code == 204:
                    flash('Кассир успешно уволен', "info")
                    response = redirect(url_for('kassirs.get_all'))
                    return response
                elif result.response.status_code == 403:
                    do_logout()
                    return redirect(url_for('users.login'))
                else:
                    flash("Кассир не найден", "error")
                    return redirect(url_for('kassirs.get_all'))
            else:
                flash(result.error, "error")
                return redirect(url_for('kassirs.get_all'))


@mod.route('/kassirs/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('kassirs.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_kassir(page, 10, request.cookies)
        if result.success:
            if result.response.status_code == 200:
                kassirs_obj = result.response.content
                kassirs_str = (str(kassirs_obj)).split('\\n')
                n = len(kassirs_str)
                kassirs_str.remove(kassirs_str[0])
                n = n-1
                kassirs_str[n-1] = kassirs_str[n-1][0:-1]
                kassirs = []
                dictr = json.loads(kassirs_str[n-1])
                kassirs_str.remove(kassirs_str[n-1])
                for kassir in kassirs_str:
                    kassir1 = bytes(kassir, 'utf8')
                    kassirs.append(json.loads(kassir1))
                return render_template("/kassirs/get_all.html", kassirs=kassirs, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash("Кассир не найден", "error")
                return redirect(url_for('kassirs.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('kassirs.index'))