from flask import Flask
import os,sys
sys.path.insert(0, os.path.abspath(".."))

app = Flask(__name__)
app.secret_key = 'koech'

from views import user
from entries.views import apps
from routes import main
#from users.views import Users

import jwt



app.register_blueprint(user)
app.register_blueprint(apps)
app.register_blueprint(main)

