from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort

mod = Blueprint('menu', __name__)


@mod.route('/')
def index():
    if not hasattr(g, 'logged_in'):
        g.logged_in = False
    if g.logged_in:
        return render_template("index.html")
    else:
        return redirect(url_for('users.login'))