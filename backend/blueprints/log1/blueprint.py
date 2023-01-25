from flask import Flask,Blueprint
from pymongo import MongoClient
import hashlib
from flask import Flask, request, jsonify
from flask_jwt_extended import unset_jwt_cookies, jwt_required,create_access_token,get_jwt_identity
import datetime
import hashlib

client = MongoClient('localhost', 27017)
log_system = Blueprint('log', __name__)
db = client['system']
users_collection = db['user']

@log_system.before_request
def before_request():
    db.logs.insert_one({"timestamp": datetime.datetime.now(), "method": request.method, "endpoint": request.url})