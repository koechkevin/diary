from flask import *
import datetime
import jwt
import psycopg2
import re
import base64
import hashlib

from diary_model import db_model

app = Flask(__name__)

app.secret_key="koech"


connection=connection=db_model.connection 


def authorize(token):
    output=True
    if token is None or token=='':
        return False
    sql="select token from blacklist where token='"+token+"';"
    cursor=connection.cursor()
    cursor.execute(sql)
    resultSet=cursor.fetchall()
    for each in resultSet:
        if each[0]==token:
            output=False
    return output

def validEmail(email):
    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
        return True
    return False

@app.route('/')
def home():
    
    return "welcome to my diary",200

@app.route('/api/v2/register',methods=['POST'])
def register():
    connection.commit()
    data = request.get_json()
    fname=data['fname']
    lname=data['lname']
    email=data['email']
    username=data['username']
    password=hashlib.sha256(base64.b64encode(bytes(data['password'],'utf-8'))).hexdigest()
    confirm_password=hashlib.sha256(base64.b64encode(bytes(data['cpassword'],'utf-8'))).hexdigest()
    cursor=connection.cursor()
    sql1="INSERT INTO users \
    (name,email,username,password) VALUES \
    ('"+fname+" "+lname+"','"+email+"',\
    '"+username+"','"+password+"');"
    cursor.execute("select * from users where username = '"+username+"';")
    if cursor.fetchone() is not None:
        connection.commit()
        return jsonify({"message":"such user already exists"}),409
    elif password != confirm_password:
        return jsonify({"message":"password and confirm password do not match"}),403
    elif not validEmail(email):
        return jsonify("please enter a valid email"),403
    cursor.execute(sql1)
    connection.commit()
    return jsonify({"message":"You registered succesfully"}),200

@app.route('/api/v2/login',methods=['POST'])
def login():
    username=request.get_json()['username']
    password=hashlib.sha256(base64.b64encode(bytes(request.get_json()['password'],'utf-8'))).hexdigest()
    payload={}    
    sql="select * from users where username='"+username+"' and password ='"+password+"';"
    cursor=connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is None:
        return jsonify({"message":"invalid credentials"}),401
    payload={"userID":result[0],"username":username,\
             "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=15)}
    connection.commit()
    token=jwt.encode(payload,app.secret_key)
    return jsonify({"token":token.decode('utf-8')}),200



@app.route("/api/v2/account",methods=['GET'])
def account():
    if authorize(request.args.get('token')):
        try:
            userID=jwt.decode(request.args.get('token'), app.secret_key)['userID']
            sql="select * from users where id = "+str(userID)+";"
            cursor=connection.cursor()
            cursor.execute(sql)
            result=cursor.fetchone()
            name=result[1]
            email=result[2]
            username=result[3]
            output={"name":name,"email":email,"username":username,"ID":userID}
            connection.commit()
            return jsonify(output),200
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again')
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token')        
    else:
        return jsonify("you are out of session")    

@app.route('/api/v2/create_entry',methods=['POST'])
def post_entry():
    if authorize(request.args.get('token')):
        try:
            data=request.get_json()
            title=data['title']
            entry=data['entry']
            userID=jwt.decode(request.args.get('token'), app.secret_key)['userID']
            cursor=connection.cursor()
            sql="insert into entries \
            (title,entry,id)values('"+title+"','"+entry+"','"+str(userID)+"');"
            cursor.execute(sql)
            connection.commit()
            return jsonify("entry was successfully saved"),200
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again'),401
        except jwt.InvalidTokenError:
            return jsonify('invalid token'),403        
    else:
        return jsonify("you are out of session"),401

@app.route("/api/v2/entries",methods=['GET'])
def entries():
    if authorize(request.args.get('token')):
        try:
            userID=jwt.decode(request.args.get('token'), app.secret_key)['userID']
            sql="select * from entries where id = "+str(userID)+";"
            cursor=connection.cursor()
            output=[]
            cursor.execute(sql)
            result=cursor.fetchall()
            for each in result:
                output.append([str(each[0]),each[1],each[2],str(each[4])])
            connection.commit()    
            return jsonify(output),200
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again')
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token')
    else:
        return jsonify("you are out of session")    

@app.route("/api/v2/view_entry/<int:entryID>",methods=["GET"])
def view_entry(entryID):
    if authorize(request.args.get('token')):
        try:
            userID=jwt.decode(request.args.get('token'), app.secret_key)['userID']
            sql="select * from entries \
            where entryid = "+str(entryID)+" and id = "+str(userID)+";"
            cursor = connection.cursor()
            cursor.execute(sql)
            result=cursor.fetchone()
            if result is None:
                return jsonify("you are not authorized to perform this operation"),401
            connection.commit()
            return  jsonify(result[0],result[1],result[2],result[4]),200
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again')
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token')        
    else:
        return jsonify("you are out of session")    

@app.route("/api/v2/delete_entry/<int:entryId>",methods=["DELETE"])
def delete_entry(entryId):
    if authorize(request.args.get('token')):
        try:
            userID=jwt.decode(request.args.get('token'), app.secret_key)['userID']
            cursor=connection.cursor()
            sql1="select * from entries where entryid = "+str(entryId)+";"
            sql="delete from entries \
            where entryid = "+str(entryId)+" and id = "+str(userID)+";"
            cursor.execute(sql1)
            result=cursor.fetchone()
            if result is None:
                return jsonify("the entry has already been deleted")
            elif result[3]!=userID:
                return jsonify("you are not authorized to perform the operation"),401
            cursor.execute(sql)
            connection.commit()
            return jsonify("delete successful"),202
        except jwt.ExpiredSignatureError:
            return jsonify('your token expired please login again')
        except jwt.InvalidTokenError:
            return jsonify('invalid token please login to get a new token')        
    else:
        return jsonify("you are out of session")    

@app.route("/api/v2/modify_entry/<int:entryId>",methods=["PUT"])
def modify_entry(entryId):
    try:
        userID=jwt.decode(request.args.get('token'), app.secret_key)['userID']
        title=request.get_json()['title']
        entry=request.get_json()['entry']
        today=str(datetime.datetime.today()).split()
        if authorize(request.args.get('token')):
            cursor=connection.cursor()
            sqlcheck="select * from entries where entryid="+str(entryId)+";"
            cursor.execute(sqlcheck)
            result=cursor.fetchone()
            if result[3]!=userID:
                return jsonify("you are not the author of this entry") ,401
            elif str(result[4]).split()[0]!=today[0]:
                return jsonify("you can only modify an entry created today"),406
            sql="UPDATE entries SET title=\
            '"+title+"',entry='"+entry+"'where entryID="+str(entryId)+";"
            cursor.execute(sql)
            connection.commit()
            return jsonify("succesfully edited"),200
        else:
            return jsonify("you are out of session")
    except jwt.ExpiredSignatureError:
        return jsonify('your token expired please login again')
    except jwt.InvalidTokenError:
        return jsonify('invalid token please login to get a new token')        


@app.route("/api/v2/logout",methods=['GET'])
def logout():
    token=request.args.get('token')
    clearBlacklist="DELETE FROM blacklist WHERE time < NOW() - INTERVAL '30 minutes';"
    sql=" INSERT INTO blacklist(token)VALUES ('"+token+"');"
    cursor=connection.cursor()
    cursor.execute(clearBlacklist)
    cursor.execute(sql)
    connection.commit()
    return jsonify("you have been successfully logged out.Token invalidated"),200

if __name__=='__main__':
    db_model.create_table()
    app.run(port=5577,debug=True) 
