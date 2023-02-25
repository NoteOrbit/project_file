from flask import Blueprint, render_template, request, jsonify
import hashlib
from pymongo import MongoClient 
from config import client
Reg = Blueprint('Register', __name__)


@Reg.route('/Register', methods=['POST'])

def Reg1():
    _json = request.json ## user 
    _name = _json['username']
    _name1 = _json['name']
    _password = _json['password']
    _email = _json['email']
    if _name and _password and _email and _name1 and request.method == 'POST':
        _json['password'] = hashlib.sha256(_json['password'].encode('utf-8')).hexdigest()
        db = client['system']
        users_collection = db['user']
        doc = users_collection.find_one({"username": _json["username"]})
        if not doc:
        # Creating user
            users_collection.insert_one(_json)
            return jsonify({'msg': 'User created successfully'}), 201
        else:
            return jsonify({'msg': 'Username already exists'}),401
       


       


