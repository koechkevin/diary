from flask import Flask

app = Flask(__name__)
app.secret_key = 'koech'

from users.views import user
from entries.views import apps
from routes import main
#from users.views import Users

import jwt



app.register_blueprint(user)
app.register_blueprint(apps)
app.register_blueprint(main)

