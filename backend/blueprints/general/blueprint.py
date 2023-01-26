from flask import Flask, Blueprint , jsonify , request
from pymongo import MongoClient
import json

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
            user = collections.insert_one(_json)
            return jsonify('add review in db') ,201
