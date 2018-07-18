from flask import jsonify,json,Flask,request,session
import datetime
import myClass
from functools import wraps
app=Flask(__name__)
app.config["SECRET_KEY"]='kkkoech'
user_details=dict()
diary_entries=dict()


@app.route("/api/v1",methods=['GET'])
def home():
    return jsonify({"message":"welcome to my diary"})
@app.route("/api/v1/register",methods=['POST'])
def register():
    fname=request.get_json()["fname"]
    lname=request.get_json()["lname"]
    email=request.get_json()["email"]
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    cpassword=request.get_json()["cpassword"]
    if myClass.ExternalFunctions.passwordVerify(password,cpassword):
        if username not in user_details:
            user_details.update({username:{"name":fname+" "+lname,"email":email,"password":password}})
        else:
            return jsonify({"message":"such user already exists"})
    else:
        return jsonify({"message":"password and confirm password do not match"})
    return jsonify({"message":"success ! you can now login to continue"})
    

@app.route("/api/v1/login",methods=['POST'])
def login():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    if username in user_details:
        if password==user_details[username]["password"]:
            session['username']= username
            session['logged_in']=True
            return jsonify({"message":"you are successfully logged in "})
        else:
            return jsonify({"message":"wrong password,try again"})
    else:    
        return jsonify({"message":"you are not a registered user"})
def on_session(t):
    @wraps(t)
    def decorator(*args,**kwargs):
        if "logged_in" in session:
            return t(*args,**kwargs)
        else:
            return jsonify({"message":"please login first"})
    return decorator    

@app.route("/api/v1/create_entry",methods=['POST'])
@on_session
def create_entry():
    comment=request.get_json()["comment"]
    username=session.get('username')
    if username not in diary_entries:
        diary_entries.update({username:{1:str(datetime.datetime.utcnow())+" "+comment}})
    else:
        diary_entries[username].update({len(diary_entries[username])+1:str(datetime.datetime.utcnow())+" "+comment})
    return jsonify(diary_entries[username])

@app.route("/api/v1/entries",methods=['GET'])
@on_session
def entries():
    username=session.get('username')
    return jsonify(diary_entries[username])

@app.route("/api/v1/view_entry/<int:entryID>",methods=["GET"])
@on_session
def view_entry(entryID):
    username=session.get('username')
    return jsonify({"entry "+str(entryID):diary_entries[username][entryID]})

@app.route("/api/v1/delete_entry/<int:entryId>",methods=["DELETE"])
@on_session
def delete_entry(entryId):
    username=session.get('username')
    del diary_entries[username][entryId]
    return jsonify({"message":"deleted successfully"})

@app.route("/api/v1/modify_entry/<int:entryId>",methods=["PUT"])
def modify_entry(entryId):
    comment=request.get_json()["comment"]
    username=session.get('username')
    del diary_entries[username][entryId]
    diary_entries[username].update({entryId:str(datetime.datetime.utcnow())+" "+comment})
    return jsonify({"message":"successfully edited an entry"})

@app.route("/api/v1/account",methods=['GET'])
def account():
    username=session.get('username')
    myDetails={"name":user_details[username]['name'],"email":user_details[username]['email']}
    return jsonify(myDetails)


@app.route("/api/v1/logout",methods=['GET'])
def logout():
    session.clear()
    return jsonify({"message":"successful"})

        
if __name__=='__main__':
    app.run(port=5555,debug=True) 