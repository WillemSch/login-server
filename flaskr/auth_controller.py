import flask
from flask import Flask, abort, request, send_from_directory, make_response, render_template, redirect
import flask_login
from templates.login_form import LoginForm
from templates.register_form import RegisterForm
from app import app
from random import random
from time import sleep
from flaskr.database_service import get_user, add_user
from flaskr.auth_service import login_user, user_loader
from secrets import token_hex
from hashlib import sha256


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
    if form.validate_on_submit():
        # Do a random sleep between 0 and 0.5 seconds
        sleep(.5 * random())

        username = form.username.data
        password = form.password.data
        u = get_user(username)
        if u:
            user = user_loader(u[0])
            hash = sha256((password + user.salt).encode('utf-8')).digest()
            if hash == user.passwd:
                # automatically sets logged in session cookie
                login_user(user)

                flask.flash('Logged in successfully.')

                next = flask.request.args.get('next')

                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                if False and not is_safe_url(next):
                    return flask.abort(400)

                return flask.redirect(next or flask.url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        salt = token_hex(16)
        hash = sha256((password + salt).encode('utf-8')).digest()
        add_user(username, salt, hash)

        return flask.redirect('/')
    return render_template('register.html', form=form)
