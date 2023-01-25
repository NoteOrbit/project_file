from flask import Flask, jsonify, request , Blueprint
from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["system"]
logs_collection = db["logs"]

logs_bp = Blueprint('logs', __name__)

@logs_bp.before_request
def before_request():
    db.logs.insert_one({"timestamp": datetime.datetime.now(), "method": request.method, "endpoint": request.url})
    