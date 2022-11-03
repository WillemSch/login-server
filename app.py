from flask import Flask
from threading import local
from secrets import token_bytes

tls = local()

# Set up app
app = Flask(__name__)
# use a secure randon token as secret key
app.secret_key = token_bytes(16)


# import Services and Controllers
import flaskr.database_service
import flaskr.auth_service
import flaskr.index_controller
import flaskr.auth_controller
import flaskr.messager_controller
import flaskr.api_controller

flaskr.database_service.setup()
