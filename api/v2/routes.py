"""
The module initializes the home page route
"""
from flask import Blueprint, jsonify

main = Blueprint("main", __name__)

@main.route("/api/v2/", methods=['GET'])
def home():
    """
The landing page route
"""
    return jsonify("welcome to my diary"), 200
