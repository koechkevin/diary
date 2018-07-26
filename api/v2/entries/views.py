import datetime
import os,sys
sys.path.insert(0, os.path.abspath(".."))
import jwt
from functools import wraps

from flask import *
from models import *
from __init__ import *


apps = Blueprint("entries", __name__)
connection = DatabaseModel.connection

class Entries():
    
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
       
    def on_session(t):
        @wraps(t)
        def auth(*args, **kwargs):
            if not Entries.authorize(request.args.get('token')):
                return jsonify("you are out of session")
            try:
                data = jwt.decode(request.args.get('token'), "koech")
            except jwt.ExpiredSignatureError:
                return jsonify('your token expired please login again')
            except jwt.InvalidTokenError:
                return jsonify('invalid token please login to get a new token')
            return t(*args, **kwargs)
        return auth
    
    # creates user entries
    @apps.route('/api/v2/entries/create_entry', methods=['POST'])
    @on_session
    def post_entry():
            try:
                data = request.get_json()
                title = data['title']
                entry = data['entry']
                if title.strip() == '' or entry.strip() == '':
                    return jsonify('title and entry cannot be empty'), 422            
                user_id = jwt.decode(request.args.get('token'), app.secret_key)['user_id']
                cursor = connection.cursor()
                sql = "insert into entries \
                (title,entry,id)values('"+title+"','"+entry+"','"+str(user_id)+"');"
                cursor.execute(sql)
                connection.commit()
                return jsonify("entry was successfully saved"), 200
            except KeyError:
                return jsonify('provide title and entry to be saved'), 422
    
      # a user can view all entries  
    @apps.route("/api/v2/entries", methods=['GET'])
    @on_session
    def entries():
            user_id = jwt.decode(request.args.get('token'), app.secret_key)['user_id']
            sql = "select * from entries where id = "+str(user_id)+";"
            cursor = connection.cursor()
            output = []
            cursor.execute(sql)
            result = cursor.fetchall()
            for each in result:
                output.append([str(each[0]),each[1],each[2],str(each[4])])
            connection.commit()    
            return jsonify(output), 200
    
    #user views a single entry
    @apps.route("/api/v2/entries/view_entry/<int:entry_id>", methods=["GET"])
    @on_session
    def view_entry(entry_id):
            user_id = jwt.decode(request.args.get('token'), app.secret_key)['user_id']
            sql = "select * from entries \
            where entryid = "+str(entry_id)+" and id = "+str(user_id)+";"
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                return jsonify("entry id "+str(entry_id)+" is \
                not part of your entries . you can only view your entries"), 401
            connection.commit()
            return  jsonify(result[0],result[1],result[2],result[4]), 200
            
    #a user can edit an entry made today
    @apps.route("/api/v2/entries/modify_entry/<int:entry_id>", methods=["PUT"])
    @on_session
    def modify_entry(entry_id):
        try:
            user_id = jwt.decode(request.args.get('token'), app.secret_key)['user_id']
            title = request.get_json()['title']
            entry = request.get_json()['entry']
            if title.strip() == '' or entry.strip() == '':
                return jsonify('title and entry cannot be empty'),422
            today = str(datetime.datetime.today()).split()
            if Entries.authorize(request.args.get('token')):
                cursor = connection.cursor()
                sqlcheck = "select * from entries where entryid="+str(entry_id)+";"
                cursor.execute(sqlcheck)
                result = cursor.fetchone()
                if result[3] != user_id:
                    return jsonify("you are not the author of this entry"), 401
                elif str(result[4]).split()[0] != today[0]:
                    return jsonify("you can only modify an entry created today"), 406
                sql = "UPDATE entries SET title=\
                '"+title+"',entry='"+entry+"'where entryID="+str(entry_id)+";"
                cursor.execute(sql)
                connection.commit()
                return jsonify("succesfully edited"), 200
            return jsonify("you are out of session")
        except KeyError:
            return jsonify('provide new title and new entry to replace'), 422
        
        
        # a user can delete his entry
    @apps.route("/api/v2/entries/delete_entry/<int:entry_id>", methods=["DELETE"])
    @on_session
    def delete_entry(entry_id):
            user_id = jwt.decode(request.args.get('token'), app.secret_key)['user_id']
            cursor = connection.cursor()
            sql1 = "select * from entries where entryid = "+str(entry_id)+";"
            sql = "delete from entries \
            where entryid = "+str(entry_id)+" and id = "+str(user_id)+";"
            cursor.execute(sql1)
            result = cursor.fetchone()
            if result is None:
                return jsonify("the entry has already been deleted")
            elif result[3] != user_id:
                return jsonify("you are not authorized to perform the operation"), 401
            cursor.execute(sql)
            connection.commit()
            return jsonify("delete successful"), 202