import datetime
import re
import base64
import hashlib
import jwt

from flask import jsonify, Flask, request
from diary_model import db_model

app = Flask(__name__)

app.secret_key = "koech"


connection = db_model.connection 


def authorize(token):
    output = True
    if token is None or token.strip() == '':
        return False
    sql = "select token from blacklist where token = '"+token+"';"
    cursor = connection.cursor()
    cursor.execute(sql)
    result_set = cursor.fetchall()
    for each in result_set:
        if each[0] == token:
            output = False
    return output

def valid_email(email):
    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
        return True
    return False

@app.route('/')
def home():
    
    return "welcome to my diary", 200

@app.route('/api/v2/register', methods=['POST'])
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
            return jsonify("such user already exists"), 409
        elif password != confirm_password:
            return jsonify({"message":"password and confirm password do not match"}), 403
        elif not valid_email(email):
            return jsonify("please enter a valid email"), 403
        cursor.execute(sql1)
        connection.commit()
        return jsonify({"message":"You registered succesfully"}), 200
    except KeyError:
        return jsonify('fname,lname,email,username,password,cpassword should be provided'), 422
@app.route('/api/v2/login', methods=['POST'])
def login():
    try:
        username = request.get_json()['username']
        password = hashlib.sha256(base64.b64encode\
        (bytes(request.get_json()['password'], 'utf-8'))).hexdigest()
        payload = {}    
        sql = "select * from users where username= '"+username+"' and password = '"+password+"';"
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



@app.route("/api/v2/account", methods=['GET'])
def account():
    if authorize(request.args.get('token')):
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

@app.route('/api/v2/create_entry', methods=['POST'])
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
            (title,entry,id)values('"+title+"', '"+entry+"', '"+str(user_id)+"');"
            cursor.execute(sql)
            connection.commit()
            return jsonify("entry was successfully saved"), 200
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again'), 401
        except jwt.InvalidTokenError:
            return jsonify('invalid token'), 403
        except KeyError:
            return jsonify('provide title and entry to be saved'), 422
    else:
        return jsonify("you are out of session"), 401

@app.route("/api/v2/entries", methods=['GET'])
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
                output.append([str(each[0]), each[1], each[2], str(each[4])])
            connection.commit()    
            return jsonify(output), 200
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again')
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token')
    else:
        return jsonify("you are out of session")    

@app.route("/api/v2/view_entry/<intentry_id>", methods=["GET"])
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
            return  jsonify(result[0], result[1], result[2], result[4]), 200
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again'), 403
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token'), 403        
    else:
        return jsonify("you are out of session"), 401    

@app.route("/api/v2/delete_entry/<intentry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    if authorize(request.args.get('token')):
        try:
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
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again')
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token')        
    else:
        return jsonify("you are out of session")    

@app.route("/api/v2/modify_entry/<intentry_id>", methods=["PUT"])
def modify_entry(entry_id):
    try:
        user_id = jwt.decode(request.args.get('token'), app.secret_key)['user_id']
        title = request.get_json()['title']
        entry = request.get_json()['entry']
        if title.strip() == '' or entry.strip() == '':
            return jsonify('title and entry cannot be empty'), 422
        today = str(datetime.datetime.today()).split()
        if authorize(request.args.get('token')):
            cursor = connection.cursor()
            sqlcheck = "select * from entries where entryid = "+str(entry_id)+";"
            cursor.execute(sqlcheck)
            result = cursor.fetchone()
            if result[3] != user_id:
                return jsonify("you are not the author of this entry"), 401
            elif str(result[4]).split()[0] != today[0]:
                return jsonify("you can only modify an entry created today"), 406
            sql = "UPDATE entries SET title =\
            '"+title+"',entry = '"+entry+"'where entryID = "+str(entry_id)+";"
            cursor.execute(sql)
            connection.commit()
            return jsonify("succesfully edited"), 200
        else:
            return jsonify("you are out of session")
    except jwt.ExpiredSignatureError:
        return jsonify('your token expired please login again')
    except KeyError:
        return jsonify('provide new title and new entry to replace'), 422
    except jwt.InvalidTokenError:
        return jsonify('invalid token please login to get a new token')        


@app.route("/api/v2/logout", methods=['GET'])
def logout():
    try:
        token = request.args.get('token')
        clear_blacklist = "DELETE FROM blacklist WHERE time < NOW() - INTERVAL '30 minutes';"
        sql = " INSERT INTO blacklist(token)VALUES ('"+token+"');"
        cursor = connection.cursor()
        cursor.execute(clear_blacklist)
        cursor.execute(sql)
        connection.commit()
        return jsonify("you have been successfully logged out.Token invalidated"), 200
    except TypeError:
        return jsonify('you can only logout if you were logged in'), 422

if __name__ == '__main__':
    db_model.create_table()
    app.run(port=5577, debug=True) 
