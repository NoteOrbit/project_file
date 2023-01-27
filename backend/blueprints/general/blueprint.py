from flask import Flask, Blueprint , jsonify , request
from pymongo import MongoClient
import json
import datetime
general = Blueprint("general",__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client['Infomations']

@general.route('/review',methods=['GET',"POST","UPDATE"])
def get_review():
    _json = request.json
    uid = _json['uid']
    rating = _json['rating']
    store = _json['store']
    message = _json['message']
    date = _json['date']

    if uid and rating and store and message and date and request.method == "POST":

        collections = db['User']
        user = collections.find_one({'uid':uid})
        if not user:
            return jsonify('not in db') , 401
        else:
            collections = db['Transaction']
            js = {
                "uid":uid,
                "event":"review",
                "Rating":rating,
                "Store":store,
                "Message":message,
                "Date":datetime.datetime.now(),
            }

            user = collections.insert_one(js)
            return jsonify('add review in db') ,201


@general.route('/take', methods=['GET',"POST","UPDATE"])
def take():

    db = client['Infomations']
    _json = request.json
    users_collection = db['User']
    name = _json['name']
    gender = _json['gender']
    age = _json['age']
    uid = _json['uid']

   
    if name and gender and age and uid and request.method == "POST":
        _json = request.json
        doc = users_collection.find_one({"name": _json["name"]})
        if doc:
            return jsonify({'msg': 'exctied'}), 401
        
        users_collection.insert_one(_json)
        return jsonify({'msg': 'add user'}), 201