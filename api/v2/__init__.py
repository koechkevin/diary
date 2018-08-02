"""
    module registers blueprint and defines variable app to be used in run.py
    """
import os
import sys
import jwt

from flask import Flask
#from flask_cors import CORS
from users.views import USER
from entries.views import APPS
from routes import MAIN

sys.path.insert(0, os.path.abspath(".."))


APP = Flask(__name__)
#CORS(APP)
APP.secret_key = 'koech'

APP.register_blueprint(USER)
APP.register_blueprint(APPS)
APP.register_blueprint(MAIN)
