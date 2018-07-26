import datetime
import hashlib
import re
import base64
import jwt

from flask import *
from models import *
from __init__ import *


users = Blueprint("users", __name__)
connection = DatabaseModel.connection

class Users():
    def __init__(self):
        pass
    def authorize(token):
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
    
    def valid_email(email):
        if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
            return True
        return False
    
    @users.route('/api/v2/users/register', methods=['POST'])
    def register():
        try:
            connection.commit()
            data = request.get_json()
            fname = data['fname']
            lname = data['lname']
            email = data['email']
            username = data['username']
            password = hashlib.sha256(base64.b64encode\
            (bytes(data['password'], 'utf-8'))).hexdigest()
            confirm_password = hashlib.sha256(base64.b64encode\
            (bytes(data['cpassword'], 'utf-8'))).hexdigest()
            if fname.strip() == '' or lname.strip() == '' or password.strip() == '':
                return jsonify('Fields cannot be empty'), 422
            cursor = connection.cursor()
            sql1 = "INSERT INTO users \
            (name, email, username, password) VALUES \
            ('"+fname+" "+lname+"', '"+email+"',\
            '"+username+"', '"+password+"');"
            cursor.execute("select * from users where username = '"+username+"';")
            if cursor.fetchone() is not None:
                connection.commit()
                return jsonify({"message":"such user already exists"}), 409
            elif password != confirm_password:
                return jsonify({"message":"password and confirm password do not match"}), 403
            elif not Users.valid_email(email):
                return jsonify("please enter a valid email"), 403
            cursor.execute(sql1)
            connection.commit()
            return jsonify({"message":"You registered succesfully"}), 200
        except KeyError:
            return jsonify('fname, lname, email, username, password, cpassword should be provided'), 422
        
    @users.route('/api/v2/users/login', methods=['POST'])
    def login():
        try:
            username = request.get_json()['username']
            password = hashlib.sha256(base64.b64encode\
            (bytes(request.get_json()['password'], 'utf-8'))).hexdigest()
            payload = {}
            sql = "select * from users where username='"+username+"' and password ='"+password+"';"
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                return jsonify({"message":"invalid credentials"}), 401
            payload = {"user_id":result[0], "username":username, \
                     "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=15)}
            connection.commit()
            token = jwt.encode(payload, app.secret_key)
            return jsonify({"token":token.decode('utf-8')}), 200
        except KeyError:
            return jsonify('username and password should be provided in a json format'), 422
        
    @users.route("/api/v2/users/account", methods=['GET'])
    def account():
        if Users.authorize(request.args.get('token')):
            try:
                user_id = jwt.decode(request.args.get('token'), app.secret_key)['user_id']
                sql = "select * from users where id = "+str(user_id)+";"
                cursor = connection.cursor()
                cursor.execute(sql)
                result = cursor.fetchone()
                name = result[1]
                email = result[2]
                username = result[3]
                output = {"name":name, "email":email, "username":username, "ID":user_id}
                connection.commit()
                return jsonify(output), 200
            except jwt.ExpiredSignatureError:
                return jsonify('your token expired please login again')
            except jwt.InvalidTokenError:
                return jsonify('invalid token please login to get a new token')        
        else:
            return jsonify("you are out of session")        
        
    @users.route("/api/v2/users/logout", methods=['GET'])
    def logout():
        try:
            token = request.args.get('token')
            clear = "DELETE FROM blacklist WHERE time < NOW() - INTERVAL '30 minutes';"
            sql = " INSERT INTO blacklist(token)VALUES ('"+token+"');"
            cursor = connection.cursor()
            cursor.execute(clear)
            cursor.execute(sql)
            connection.commit()
            return jsonify("you have been successfully logged out.Token invalidated"), 200
        except TypeError:
            return jsonify('you can only logout if you were logged in'), 422