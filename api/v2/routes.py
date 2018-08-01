from flask import Blueprint, jsonify

main = Blueprint("main", __name__)

@main.route("/api/v2/", methods=['GET'])
def home():
    return jsonify("welcome to my diary"), 200
