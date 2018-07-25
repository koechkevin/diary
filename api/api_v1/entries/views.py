from flask import *

apps = Blueprint("entries", __name__)

#class Entries():
def authorize(token):
    output = True
    if token is None or token.strip() == '':
        return False
    sql = "select token from blacklist where token='"+token+"';"
    cursor = connection.cursor()
    cursor.execute(sql)
    resultS = cursor.fetchall()
    for each in resultSet:
        if each[0] == token:
            output = False
    return output

def valid_email(email):
    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
        return True
    return False    
# creates user entries
@apps.route('/api/v2/entries/create_entry', methods=['POST'])
def post_entry():
    if authorize(request.args.get('token')):
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
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again'), 401
        except jwt.InvalidTokenError:
            return jsonify('invalid token'), 403
        except KeyError:
            return jsonify('provide title and entry to be saved'), 422
    return jsonify("you are out of session"), 401
  # a user can view all entries  
@apps.route("/api/v2/entries", methods=['GET'])
def entries():
    if authorize(request.args.get('token')):
        try:
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
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again')
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token')
    return jsonify("you are out of session")

#user views a single entry
@apps.route("/api/v2/entries/view_entry/<int:entry_id>", methods=["GET"])
def view_entry(entry_id):
    if authorize(request.args.get('token')):
        try:
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
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again'), 403
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token'), 403        
    return jsonify("you are out of session"), 401
#a user can edit an entry made today
@apps.route("/api/v2/entries/modify_entry/<int:entryId>", methods=["PUT"])
def modify_entry(entryId):
    try:
        user_id = jwt.decode(request.args.get('token'), app.secret_key)['userID']
        title = request.get_json()['title']
        entry = request.get_json()['entry']
        if title.strip() == '' or entry.strip() == '':
            return jsonify('title and entry cannot be empty'),422
        today = str(datetime.datetime.today()).split()
        if authorize(request.args.get('token')):
            cursor = connection.cursor()
            sqlcheck = "select * from entries where entryid="+str(entryId)+";"
            cursor.execute(sqlcheck)
            result = cursor.fetchone()
            if result[3] != userID:
                return jsonify("you are not the author of this entry"), 401
            elif str(result[4]).split()[0] != today[0]:
                return jsonify("you can only modify an entry created today"), 406
            sql = "UPDATE entries SET title=\
            '"+title+"',entry='"+entry+"'where entryID="+str(entryId)+";"
            cursor.execute(sql)
            connection.commit()
            return jsonify("succesfully edited"), 200
        return jsonify("you are out of session")
    except jwt.ExpiredSignatureError:
        return jsonify('your token expired please login again')
    except KeyError:
        return jsonify('provide new title and new entry to replace'), 422
    except jwt.InvalidTokenError:
        return jsonify('invalid token please login to get a new token')
    # a user can delete his entry
@apps.route("/api/v2/entries/delete_entry/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    if authorize(request.args.get('token')):
        try:
            user_id = jwt.decode(request.args.get('token'), app.secret_key)['user_id']
            cursor = connection.cursor()
            sql1 = "select * from entries where entryid = "+str(entry_id)+";"
            sql = "delete from entries \
            where entryid = "+str(entry_id)+" and id = "+str(userI_id)+";"
            cursor.execute(sql1)
            result = cursor.fetchone()
            if result is None:
                return jsonify("the entry has already been deleted")
            elif result[3] != user_id:
                return jsonify("you are not authorized to perform the operation"), 401
            cursor.execute(sql)
            connection.commit()
            return jsonify("delete successful"), 202
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again')
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token')        
    return jsonify("you are out of session")        