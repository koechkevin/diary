from flask import Flask

app = Flask(__name__)
app.secret_key='koech'

from users.views import users
from entries.views import apps
from routes import main

app.register_blueprint(users)
app.register_blueprint(apps)
app.register_blueprint(main)
