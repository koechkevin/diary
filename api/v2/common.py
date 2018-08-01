"""
module contains functions that are  shared by views
"""
from functools import wraps

import re
import jwt
from flask import request, Flask, jsonify
from models import DatabaseModel

connection = DatabaseModel.connection

class Common():
    """
class contains all required methods
"""
    def __init__(self):
        pass
    def authorize(self, token):
        """
method checks if a user has been logged out or has been blacklisted
"""
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
        """
method checks validity of a supplied email
"""
        if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
            return True
        return False
    def on_session(t):
        """
defines decorator to authorise a user on session
"""
        @wraps(t)
        def auth(*args, **kwargs):
            if not Common().authorize(request.headers.get('x-access-token')):
                return jsonify({"message":"you are out of session"})
            try:
                jwt.decode(request.headers.get('x-access-token'), "koech")
            except jwt.ExpiredSignatureError:
                return jsonify({"message":'your token expired please login again'})
            except jwt.InvalidTokenError:
                return jsonify({"message":'invalid token please login to get a new token'})
            return t(*args, **kwargs)
        return auth
