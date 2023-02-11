from flask import Flask, Blueprint , jsonify , request , current_app
from pymongo import MongoClient
import pandas as pd
import json
import datetime
import hashlib
from config import client
general = Blueprint("general",__name__)

# client = MongoClient("mongodb://0.tcp.ap.ngrok.io:17474")

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
            collections2 = db['Transaction_user']
            js = {
                "uid":uid,
                "event":"review",
                "Rating":rating,
                "Store":store,
                "Message":message,
                "Date":datetime.datetime.now(),
            }

            user = collections.insert_one(js)
            user = collections.find({"uid":uid,"Store":store,"event":"review"},{'Store':1, '_id':0,'uid':1,'Rating':1,"Message":1})
            if user:
                df12 =  pd.DataFrame(list(user))
                dfadd = {
                    "Store":df12["Store"].values[0],
                    "User":df12['uid'].values[0],
                    "Rating":df12['Rating'].values[0],
                    "Review":df12['Message'].values[0]
                }
                print(dfadd)
                martix = collections2.insert_one(dfadd)

            return jsonify('add review in db') ,201
            

@general.route('/take', methods=['GET',"POST","UPDATE"]) ## regiseter
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
    

@general.route('/take2', methods=['GET',"POST","UPDATE"]) ## event
def take2():
    db = client['Infomations']
    _json = request.json
    uid = _json['uid']
    event = _json['event']
    Content = _json['Content']
    users_collection = db['Transactions']
    hash_object = hashlib.sha256(current_app.config['path'].encode())
    hex_dig = hash_object.hexdigest()
    js = {
                
                "uid":uid,
                "event":event,
                "Content":Content,
                "Date":datetime.datetime.now(),
                "Path":current_app.config['path'],
                "recomend_id":hex_dig
            }

    user = users_collection.insert_one(js)
    return jsonify({'msg': 'log save'}), 201


@general.route('/overview', methods=['GET',"POST","UPDATE"]) ## event
def overview():
    db = client['Infomations']
    _json = request.json
    uid = _json['uid']
    event = _json['event']
    Content = _json['Content']
    users_collection = db['Transactions']
    hash_object = hashlib.sha256(current_app.config['path'].encode())
    hex_dig = hash_object.hexdigest()
    js = {
                
                "uid":uid,
                "event":event,
                "Content":Content,
                "Date":datetime.datetime.now(),
                "Path":current_app.config['path'],
                "recomend_id":hex_dig
            }

    user = users_collection.insert_one(js)
    return jsonify({'msg': 'log save'}), 201