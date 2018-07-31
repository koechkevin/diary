from flask import jsonify, request, Flask, Blueprint, make_response, abort
from models import *
from __init__ import *
from functools import wraps
from flask_restful import Api, Resource
from common import Common

import os,sys
sys.path.insert(0, os.path.abspath(".."))
import datetime
import hashlib
import re
import base64
import jwt


user = Blueprint("users", __name__)
api = Api(user)


connection = DatabaseModel.connection

    
class UserLogin(Resource):
    def post(self):
        try:
            username = request.get_json()['username']
            password = hashlib.sha256(base64.b64encode\
            (bytes(request.get_json()['password'], 'utf-8'))).hexdigest()
        except KeyError:
            abort(422)
            return jsonify('username and password should be provided in a json format')
        payload = {}
        sql = "select * from users where username='"+username+"' and password ='"+password+"';"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            return jsonify({"message":"invalid credentials"})
        payload = {"user_id":result[0], "username":username, \
                 "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=15)}
        connection.commit()
        token = jwt.encode(payload, app.secret_key)
        return jsonify({"token":token.decode('utf-8')})
 
class UserLogout(Resource):   
    @Common.on_session
    def get(self):
        try:
            token = request.headers.get('x-access-token')
            clear = "DELETE FROM blacklist WHERE time < NOW() - INTERVAL '30 minutes';"
            sql = " INSERT INTO blacklist(token)VALUES ('"+token+"');"
            cursor = connection.cursor()
            cursor.execute(clear)
            cursor.execute(sql)
            connection.commit()
            return jsonify("you have been successfully logged out.Token invalidated")
        except TypeError:
            return jsonify('you can only logout if you were logged in')
        
class UserRegister(Resource):
    def valid_password(self, password):
        if re.match("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            return True
        return False
    def post(self):
        try:
            connection.commit()
            data = request.get_json()
            fname = data['fname']
            lname = data['lname']
            email = data['email']
            username = data['username']
            raw_pass = data['password']
            if not UserRegister().valid_password(raw_pass):
                return jsonify('password should be 8 characters long with both numbers and letters')
            password = hashlib.sha256(base64.b64encode\
            (bytes(raw_pass, 'utf-8'))).hexdigest()
            confirm_password = hashlib.sha256(base64.b64encode\
            (bytes(data['cpassword'], 'utf-8'))).hexdigest()
        except KeyError:
            abort(422)
            return jsonify('fname, lname, email, username, password, cpassword should be provided')         
        if fname.strip() == '' or lname.strip() == '' or username.strip() == '':
            return jsonify('Fields cannot be empty')
        cursor = connection.cursor()
        sql1 = "INSERT INTO users \
        (name, email, username, password) VALUES \
        ('"+fname+" "+lname+"', '"+email+"',\
        '"+username+"', '"+password+"');"
        cursor.execute("select * from users where username = '"+username+"';")
        result = cursor.fetchone()
        cur = connection.cursor()
        cur.execute("select * from users where email = '"+email+"';")
        res = cur.fetchone()
        if result is not None or res is not None:
            connection.commit()
            abort(409)
            return jsonify("email or username already exists")
        elif password != confirm_password:
                return jsonify({"message":"password and confirm password do not match"})
        elif not Common().valid_email(email):
            #abort(406)
            return jsonify("please enter a valid email")
        cursor.execute(sql1)
        connection.commit()
        return jsonify({"message":"You registered succesfully"})
        
    @Common.on_session    
    def get(self):
        user_id = jwt.decode(request.headers.get('x-access-token'), app.secret_key)['user_id']
        sql = "select * from users where id = "+str(user_id)+";"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        name = result[1]
        email = result[2]
        username = result[3]
        output = {"name":name, "email":email, "username":username, "ID":user_id}
        connection.commit()
        return jsonify(output)

api.add_resource(UserLogin, '/api/v2/users/login')
api.add_resource(UserLogout, '/api/v2/users/logout')
api.add_resource(UserRegister, '/api/v2/users/register')
