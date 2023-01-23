from flask import Flask,Blueprint
from pymongo import MongoClient
import hashlib
from flask import Flask, request, jsonify
from flask_jwt_extended import unset_jwt_cookies, jwt_required,create_access_token
import datetime
import hashlib
import urllib
import jwt


client = MongoClient('localhost', 27017)
login1 = Blueprint('login', __name__)
db = client['system']
users_collection = db['user']

@login1.route('/login', methods=['POST'])
def login():
    # Getting the login Details from payload
    login_details = request.get_json() # store the json body request
    # Checking if user exists in database or not
    user_from_db = users_collection.find_one({'username': login_details['username']})  # search for user in database
    # If user exists
    if user_from_db:
        # Check if password is correct
        encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            # Create JWT Access Token
            access_token = create_access_token(identity=user_from_db['username']) # create jwt token
            # Return Token

            return jsonify(access_token=access_token, token=access_token), 200
    return jsonify({'msg': 'The username or password is incorrect'}), 401
