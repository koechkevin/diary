from functools import wraps
import jwt
from flask import *
from models import *
import re
connection = DatabaseModel.connection
class Common():
    def __init__(self):
        pass
    
    def authorize(self, token):
        output = True
        if token is None or token.strip() == '':
            return False
        sql = "select token from blacklist where token='"+token+"';"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for each in result:
            if each[0] == token:
                output = False
        return output
    
    def valid_email(self, email):
        if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
            return True
        return False
    
    def on_session(t):
        @wraps(t)
        
        def auth(*args, **kwargs):
            if not Common().authorize(request.args.get('token')):
                return jsonify("you are out of session")
            try:
                data = jwt.decode(request.args.get('token'), "koech")
            except jwt.ExpiredSignatureError:
                return jsonify('your token expired please login again')
            except jwt.InvalidTokenError:
                return jsonify('invalid token please login to get a new token')
            return t(*args, **kwargs)
        return auth