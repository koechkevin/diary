from flask import Flask, request, Blueprint

main = Blueprint("main", __name__)

@main.route("/api/v2/", methods=['GET'])
def home():
    return "welcome to my diary", 200
