from app import app
from base64 import b64decode
from http import HTTPStatus
from flask import abort
from werkzeug.datastructures import WWWAuthenticate
from flaskr.database_service import get_user_by_id, get_user
from hashlib import sha256

import flask_login
from flask_login import login_required, login_user
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Class to store user info
# UserMixin provides us with an `id` field and the necessary
# methods (`is_authenticated`, `is_active`, `is_anonymous` and `get_id()`)
class User(flask_login.UserMixin):
    pass


# This method is called whenever the login manager needs to get
# the User object for a given user id
@login_manager.user_loader
def user_loader(user_id):
    result = get_user_by_id(user_id)
    if result is None:
        return
    user = User()
    user.id = result[0]
    user.name = result[1]
    user.salt = result[2]
    user.passwd = result[3]
    return user


# This method is called to get a User object based on a request,
# for example, if using an api key or authentication token rather
# than getting the user name the standard way (from the session cookie)
@login_manager.request_loader
def request_loader(request):
    print('using this')
    # Even though this HTTP header is primarily used for *authentication*
    # rather than *authorization*, it's still called "Authorization".
    auth = request.headers.get('Authorization')

    # If there is not Authorization header, do nothing, and the login
    # manager will deal with it (i.e., by redirecting to a login page)
    if not auth:
        return

    (auth_scheme, auth_params) = auth.split(maxsplit=1)
    auth_scheme = auth_scheme.casefold()
    if auth_scheme == 'basic':  # Basic auth has username:password in base64
        (uid,passwd) = b64decode(auth_params.encode(errors='ignore')).decode(errors='ignore').split(':', maxsplit=1)
        # print(f'Basic auth: {uid}:{passwd}')
        u = get_user(uid)
        u = user_loader(u[0])
        if u: # and check_password(u.password, passwd):
            hash = sha256((passwd + u.salt).encode('utf-8')).digest()
            if hash == u.passwd:
                return u
    abort(HTTPStatus.UNAUTHORIZED, www_authenticate = WWWAuthenticate('Basic realm=inf226, Bearer'))
