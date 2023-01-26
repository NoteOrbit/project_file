from flask import Flask,Blueprint
from pymongo import MongoClient
import hashlib
from flask import Flask, request, jsonify
from flask_jwt_extended import unset_jwt_cookies, jwt_required,create_access_token,get_jwt_identity
from datetime import datetime, timedelta
import hashlib
import json


client = MongoClient('localhost', 27017)
db = client['system']
users_collection = db['logs']

log_system = Blueprint('log_system', __name__)


@log_system.route('/logbox', methods=['GET'])
def log_box():
    pipeline = [
        {"$group":{"_id":"$method","count":{"$sum":1}}},
        {"$sort":{"count":-1}}
    ]

    total = users_collection.aggregate(pipeline)
    messs = {
        "data":[x for x in total]
    }
    sb = json.dumps(messs)
    s = json.loads(sb)

    return jsonify(s), 200

@log_system.route('/7day', methods=['GET'])
def get_last_7_days_logs():


    pipeline = [
        {"$match": {"timestamp": {"$gte": datetime.now() - timedelta(days=7)}}},
        {
            "$group": {
                "_id": {
                    "dayOfWeek": {"$dayOfWeek": "$timestamp"},
                    "method": "$method"
                },
                "count": {"$sum": 1}
            }
        }
    ]
    # Execute the aggregate function
    logs = list(users_collection.aggregate(pipeline))
    return jsonify(logs)