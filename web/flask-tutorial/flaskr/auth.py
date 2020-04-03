import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST', 'GET'))
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
        elif db.execute('select id from user where username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered'.format(username)

        if error is None:
            db.execute('insert into user (username,password) values (?,?)',
                       (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
        user = db.execute('select * from user where username = ?',
                          (username,)).fetchone()
        if user is None:
            error = 'login error,check username or password'
        elif check_password_hash(user['password'], password):
            error = 'login error,check username or password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('select * from user where id = ?', (user_id,)).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    def wrapped_view(**kwargs):
        if g.user is None:
            redirect(url_for('index'))
        return view(**kwargs)

    return wrapped_view
