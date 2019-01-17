from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_create_mag, do_get_paginated_mag, do_get_mag, do_logout
import json

mod = Blueprint('mags', __name__)


@mod.route('/mags/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    return render_template("/mags/index.html")


@mod.route('/mags/get/<mag_id>', methods=['GET', 'POST'])
def get(mag_id):
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        result = do_get_mag(mag_id, request.cookies)
        if result.success:
            if result.response.status_code == 200:
                tmp = str(result.response.content)
                list_sm = tmp.split('\\n')
                mag = list_sm[0]
                mag = mag[2:]
                kassir = list_sm[1]
                kassir = kassir[0:-1]
                mag_d = json.loads(mag)
                datetime = str(mag_d["datetime"]).split("_")
                date = datetime[0]
                time = datetime[1]
                dictionary = {"date":date, "time":time}
                ar = mag_d["seats"]
                kassir_d = json.loads(kassir)
                return render_template("/mags/get.html", mag=mag_d, kassir=kassir_d, seats = ar,
                                       datetime = dictionary, number_of_seats = len(ar)+1)
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash('Ошибка. Кассира магазина не существует.', "error")
                return redirect(url_for('mags.get_all'), "error")
        else:
            flash(result.error, "error")
            return redirect(url_for('mags.get_all'), "error")


@mod.route('/mags/create', methods=['GET', 'POST'])
def create():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'kassir_id' in request.args:
            kassir_id = request.args['kassir_id']
            return render_template("/mags/create.html", kassir_id=kassir_id)
    else:
        failed = False
        if 'number_of_seats' not in request.form or request.form['number_of_seats']=='':
            flash('Количество товара не задано', "error")
            failed = True
        try:
            number_of_seats = int(request.form['number_of_seats'])
        except:
            flash('Количество товара выражается числом', 'error')
            return render_template("/mags/create.html", kassir_id=request.args['kassir_id'])

        if 'date' not in request.form or request.form['date']=='':
            flash('Дата не задана', "error")
            failed = True

        if 'time' not in request.form or request.form['time']=='':
            flash('Время задано', "error")
            failed = True
        date_time = request.form['date'] + '_' + request.form['time']

        if failed:
            return render_template("/mags/create.html", kassir_id=request.args['kassir_id'])

        result = do_create_mag(request.args['kassir_id'], number_of_seats, date_time, request.cookies)
        if result.success:
            if result.response.status_code == 201:
                flash('Витрина в магазине успешно создана', "info")
                response = redirect('kassirs/get_all')
                return response
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                st = result.response.content.decode('utf-8')
                if st=='':
                    st = str(result.response.content)
                flash(st, "error")
                return redirect(url_for('kassirs.get_all'))
        else:
            flash(result.error)
            return redirect(url_for('kassirs/get_all'), "error")


@mod.route('/mags/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('mags.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_mag(page, 10, request.cookies)
        if result.success:
            if result.response.status_code == 200:
                mags_obj = result.response.content
                mags_str = (str(mags_obj)).split('\\n')
                n = len(mags_str)
                mags_str[0] = mags_str[0][2:]
                mags_str[n-1] = mags_str[n-1][0:-1]
                mags = []
                dictr = json.loads(mags_str[n-1])
                mags_str.remove(mags_str[n-1])
                for mag in mags_str:
                    if mag != "":
                        mag1 = json.loads(bytes(mag, 'utf8'))
                        ar = mag1["seats"]
                        number_of_seats = len(ar)
                        number_of_free_seats = 0
                        for item in ar:
                            if item:
                                number_of_free_seats = number_of_free_seats+1
                        datetime = str(mag1["datetime"]).split("_")
                        date = datetime[0]
                        time = datetime[1]
                        dictionary = {"mag_id": mag1["mag_id"], "kassir_id": mag1["kassir_id"],
                                      "number_of_seats": number_of_seats, "number_of_free_seats": number_of_free_seats,
                                      "date":date, "time":time}
                        mags.append(dictionary)
                return render_template("/mags/get_all.html", mags=mags, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash("Магазины не найдены", "error")
                return redirect(url_for('mags.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('mags.index'))