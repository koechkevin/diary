"""
    module registers blueprint and defines variable app to be used in run.py
    """
import os
import sys
sys.path.insert(0, os.path.abspath(".."))
import jwt

from flask import Flask
#from flask_cors import CORS
from users.views import user
from entries.views import apps
from routes import main


app = Flask(__name__)
#CORS(app)
app.secret_key = 'koech'


app.register_blueprint(user)
app.register_blueprint(apps)
app.register_blueprint(main)

