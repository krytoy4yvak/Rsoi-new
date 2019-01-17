from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_get_paginated_prods, do_get_prod, do_buy_prod, do_return_prod, do_logout
import json

mod = Blueprint('prods', __name__)


@mod.route('/prods/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    return render_template("/prods/index.html")


@mod.route('/prods/get', methods=['GET', 'POST'])
def get():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        return render_template("/prods/get.html", prod_found = False)
    else:
        if 'prod_id' not in request.form or request.form['prod_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('prods.get'))
        else:
            prod_id = request.form["prod_id"]
            result = do_get_prod(prod_id, request.cookies)

            if result.success:
                if result.response.status_code == 200:
                    prod = json.loads(result.response.content)
                    return render_template("/prods/get.html", prod=prod, prod_found=True)
                elif result.response.status_code == 403:
                    do_logout()
                    return redirect(url_for('users.login'))
                else:
                    flash("Товар не найден", "error")
                    return redirect(url_for('prods.get'))
            else:
                flash(result.error, "error")
                return redirect(url_for('prods.get'))


@mod.route('/prods/buy')
def buy():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        mag_id = request.args['mag_id']
        seat_number = request.args['seat_number']
        result = do_buy_prod(mag_id, int(seat_number), request.cookies)
        if result.success:
            if result.response.status_code == 201:
                flash('Покупка товара успешно произведена', 'info')
                return redirect(url_for('mags.get_all'))
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash('Покупка товара не может быть произведена', 'error')
                return redirect(url_for('mags.get_all'))
        else:
            flash(result.error, 'error')
            return redirect(url_for('mags.get_all'))


@mod.route('/prods/return/<prod_id>')
def return_prod(prod_id):
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        result = do_return_prod(prod_id, request.cookies)
        if result.success:
            if result.response.status_code == 204:
                flash('Возврат товара успешно произведен', 'info')
                return redirect(url_for('menu.index'))
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash('Возврат товара не может быть произведен', 'error')
                return redirect(url_for('menu.index'))
        else:
            flash(result.error, 'error')
            return redirect(url_for('menu.index'))


@mod.route('/prods/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('prods.get_all', page=1))
        if 'submit' in request.form:
            if request.form['submit'] == 'Создать витрину':
                pass
            if request.form['submit'] == 'Уволить касира':
                pass
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_prods(page, 10, request.cookies)
        if result.success:
            if result.response.status_code == 200:
                prods_obj = result.response.content
                prods_str = (str(prods_obj)).split('\\n')
                n = len(prods_str)
                prods_str[0] = prods_str[0][2:]
                prods_str[n-1] = prods_str[n-1][0:-1]
                prods = []
                dictr = json.loads(prods_str[n-1])
                prods_str.remove(prods_str[n-1])
                for prod in prods_str:
                    if prod != '':
                        prod1 = bytes(prod, 'utf8')
                        prods.append(json.loads(prod1))
                return render_template("/prods/get_all.html", prods=prods, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash("Товары не найдены", "error")
                return redirect(url_for('prods.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('prods.index'))