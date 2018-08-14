"""
user classes
"""
import os
import sys
import datetime
import hashlib
import re
import base64
import jwt
import json

from flask import jsonify, request, Blueprint, abort
from flask_restful import Api, Resource
from models import *
#from __init__ import *
#from functools import wraps
from common import Common

sys.path.insert(0, os.path.abspath(".."))


USER = Blueprint("users", __name__)
API = Api(USER)

CONNECTION = DatabaseModel.connection

class UserLogin(Resource):
    """
    A class for login function
    """
    def post(self):
        """
    A registered user logs in
    """
        try:
            username = request.get_json()['username']
            password = hashlib.sha256(base64.b64encode\
            (bytes(request.get_json()['password'], 'utf-8'))).hexdigest()
        except KeyError:
            abort(422)
            return jsonify({"message":'username and password should be provided in a json format'})
        payload = {}
        sql = "select * from users where username='"+username+"' and password ='"+password+"';"
        cursor = CONNECTION.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            return jsonify({"message":"invalid credentials"})
        payload = {"user_id":result[0], "username":username, \
                 "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=1500)}
        CONNECTION.commit()
        token = jwt.encode(payload, 'koech')
        return jsonify({"token":token.decode('utf-8')})
class UserLogout(Resource):
    """
    A logged in user logs out and have the token invalidated
    """
    @Common.on_session
    def get(self):
        """
    log out a user
    """
        try:
            token = request.headers.get('x-access-token')
            clear = "DELETE FROM blacklist WHERE time < NOW() - INTERVAL '30 minutes';"
            sql = " INSERT INTO blacklist(token)VALUES ('"+token+"');"
            cursor = CONNECTION.cursor()
            cursor.execute(clear)
            cursor.execute(sql)
            CONNECTION.commit()
            return jsonify({"message":"you have been successfully logged out.Token invalidated"})
        except TypeError:
            return jsonify({"message":'you can only logout if you were logged in'})
class UserRegister(Resource):
    """
    A class for registration and retrieval of user details
    """
    def valid_password(self, password):
        """
    A function that checks validity of a user password on registration
    """
        if re.match("(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", password):
            return True
        return False
    def post(self):
        """
    A function that allows a user post credentials for registration
    """
        try:
            #CONNECTION.commit()
            data = request.get_json()
            #print(request.headers.get("Content-Type"))
            fname = data['fname']
            lname = data['lname']
            email = data['email']
            username = data['username']
            raw_pass = data['password']
            if not UserRegister().valid_password(raw_pass):
                return jsonify({"message"\
                :'password should be at least 8 characters long with atleast one number, one special char, one uppercase & lowercase letters'})
            password = hashlib.sha256(base64.b64encode\
            (bytes(raw_pass, 'utf-8'))).hexdigest()
            confirm_password = hashlib.sha256(base64.b64encode\
            (bytes(data['cpassword'], 'utf-8'))).hexdigest()
        except KeyError:
            abort(422)
            return jsonify({"message":'fname, lname, email, username, \
        password, cpassword should be provided'})
        if fname.strip() == '' or lname.strip() == '' or username.strip() == '':
            return jsonify({"message":'Fields cannot be empty'})
        cursor = CONNECTION.cursor()
        sql1 = "INSERT INTO users \
        (name, email, username, password) VALUES \
        ('"+fname+" "+lname+"', '"+email+"',\
        '"+username+"', '"+password+"');"
        cursor.execute("select * from users where username = '"+username+"';")
        result = cursor.fetchone()
        cur = CONNECTION.cursor()
        cur.execute("select * from users where email = '"+email+"';")
        res = cur.fetchone()
        if result is not None or res is not None:
            CONNECTION.commit()
            abort(409)
            return jsonify({"message":"email or username already exists"})
        elif password != confirm_password:
            return jsonify({"message":"password and confirm password do not match"})
        elif not Common().valid_email(email):
            #abort(406)
            return jsonify({"message":"please enter a valid email"})
        cursor.execute(sql1)
        CONNECTION.commit()
        return jsonify({"message":"You registered succesfully"})
    @Common.on_session
    def get(self):
        """
    returns details of a user on session
    """
        user_id = jwt.decode(request.headers.get('x-access-token'), 'koech')['user_id']
        sql = "select * from users where id = "+str(user_id)+";"
        cursor = CONNECTION.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        name = result[1]
        email = result[2]
        username = result[3]
        output = {"name":name, "email":email, "username":username, "ID":user_id}
        CONNECTION.commit()
        return jsonify(output)
API.add_resource(UserLogin, '/api/v2/users/login')
API.add_resource(UserLogout, '/api/v2/users/logout')
API.add_resource(UserRegister, '/api/v2/users/register')
