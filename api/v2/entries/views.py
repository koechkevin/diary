"""
    module has routes for user to perform entry operations'
    """
import datetime
import jwt
import os
import sys

from flask import jsonify, request, Flask, Blueprint, abort

sys.path.insert(0, os.path.abspath(".."))

from models import *
from __init__ import *
from flask_restful import Api, Resource
from common import Common
from functools import wraps

apps = Blueprint("entries", __name__)
api = Api(apps)

connection = DatabaseModel.connection

class CreateEntry(Resource):
    """
    class for routes '/api/v2/entries'
    """
    @Common.on_session
    def post(self):
        """
    method creates an entry'
    """
        message = ''
        try:
            data = request.get_json()
            title = data['title']
            entry = data['entry']
        except KeyError:
            abort(422)
            message = 'provide title and entry to be saved'
        if title.strip() == '' or entry.strip() == '':
            message = 'title and entry cannot be empty'
        else:
            user_id = jwt.decode(request.headers.get('x-access-token'), 'koech')['user_id']
            cursor = connection.cursor()
            sql = "insert into entries \
            (title,entry,id)values('"+title+"','"+entry+"','"+str(user_id)+"');"
            cursor.execute(sql)
            connection.commit()
            message = "entry was successfully saved"
        return jsonify({"message":message})
    #get all entries
    @Common.on_session
    def get(self):
        """
    method gets all entries a user on session has made'
    """
        user_id = jwt.decode(request.headers.get('x-access-token'), 'koech')['user_id']
        sql = "select * from entries where id = "+str(user_id)+";"
        cursor = connection.cursor()
        output = []
        cursor.execute(sql)
        result = cursor.fetchall()
        for each in result:
            output.append([str(each[0]), each[1], each[2], str(each[4])])
        connection.commit()
        return jsonify({"message":output})
class EntryId(Resource):
    """
    class for routes /api/v2/entries/<int:entry_id>
    """
    @Common.on_session
    def put(self, entry_id):
        """
    method modifies an entry
    """
        try:
            user_id = jwt.decode(request.headers.get('x-access-token'), 'koech')['user_id']
            title = request.get_json()['title']
            entry = request.get_json()['entry']
        except KeyError:
            return jsonify({"message":'provide new title and new entry to replace'})
        if title.strip() == '' or entry.strip() == '':
            return jsonify({"message":'title and entry cannot be empty'})
        today = str(datetime.datetime.today()).split()
        if Common().authorize(request.headers.get('x-access-token')):
            cursor = connection.cursor()
            sqlcheck = "select * from entries where entryid="+str(entry_id)+";"
            cursor.execute(sqlcheck)
            result = cursor.fetchone()
            if result[3] != user_id:
                return jsonify({"message":"you are not the author of this entry"})
            elif str(result[4]).split()[0] != today[0]:
                return jsonify({"message":"you can only modify an entry created today"})
            sql = "UPDATE entries SET title=\
            '"+title+"',entry='"+entry+"'where entryID="+str(entry_id)+";"
            cursor.execute(sql)
            connection.commit()
            return jsonify({"message":"succesfully edited"})
        return jsonify({"message":"you are out of session"})
     #delete an entry
    @Common.on_session
    def delete(self, entry_id):
        """
    method deletes an entry'
    """
        user_id = jwt.decode(request.headers.get('x-access-token'), 'koech')['user_id']
        cursor = connection.cursor()
        sql1 = "select * from entries where entryid = "+str(entry_id)+";"
        sql = "delete from entries \
        where entryid = "+str(entry_id)+" and id = "+str(user_id)+";"
        cursor.execute(sql1)
        result = cursor.fetchone()
        if result is None:
            return jsonify({"message":"the entry has already been deleted"})
        elif result[3] != user_id:
            return jsonify({"message":"you are not authorized to perform the operation"})
        cursor.execute(sql)
        connection.commit()
        return jsonify({"message":"delete successful"})
    #get one entry
    @Common.on_session
    def get(self, entry_id):
        """
    method gets a single entry'
    """
        user_id = jwt.decode(request.headers.get('x-access-token'), 'koech')['user_id']
        sql = "select * from entries \
        where entryid = "+str(entry_id)+" and id = "+str(user_id)+";"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            abort(401)
            return jsonify({"message":"entry id "+str(entry_id)+" is \
            not part of your entries . you can only view your entries"})
        connection.commit()
        return  jsonify({"message":[result[0], result[1], result[2], result[4]]})
api.add_resource(CreateEntry, '/api/v2/entries')
api.add_resource(EntryId, '/api/v2/entries/<int:entry_id>')
