"""
The module initializes the home page route
"""
from flask import Blueprint, jsonify

MAIN = Blueprint("main", __name__)

@MAIN.route("/api/v2/", methods=['GET'])
def home():
    """
The landing page route
"""
    return jsonify({"message":"welcome to my diary. This is it!"}), 200
