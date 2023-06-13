from flask import Flask, request, jsonify
from .database_config import User

def check_if_user_exists(email):
    user = User.query.filter_by(email = email).first()
    if user:
        return jsonify(message = 'Email has already been taken.'), 409