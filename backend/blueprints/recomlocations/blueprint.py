from math import radians, sin, cos, sqrt, atan2
from flask import Blueprint, render_template, request, jsonify 
import requests
import json
from pymongo import MongoClient 

## set up  db 
client = MongoClient('localhost', 27017)

recom_near = Blueprint('recome_near',__name__)

@recom_near.route('/recomnear',methods=['GET'])
def nearby():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    db = client['Infomations']
    collection = db['new_collection'] ## 
    
    if not all([latitude, longitude]):
        return jsonify({"error": "Missing query parameters 'latitude' and 'longitude'"}), 400
    try:
        lat = float(latitude)
        lon = float(longitude)
    except ValueError:
        return jsonify({"error": "Invalid value for 'latitude' and 'longitude'"}), 400

    results = []
    R = 6371 # radius of earth in km
    for point in collection.find({},{'_id':1,'latitude':1,'longitude':1,'store':1,'rating':1,"address	":1}):
        point_lat = point["latitude"]  ## each point
        point_lon = point["longitude"] ## each point
        dlat = radians(point_lat - lat)
        dlon = radians(point_lon - lon)
        a = sin(dlat / 2)**2 + cos(radians(lat)) * cos(radians(point_lat)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        point['distance'] = distance
        results.append(point)
    results = sorted(results, key=lambda x: x['distance'])
    for i in range(len(results)):
        results[i]['_id'] = str(results[i]['_id'])
    return jsonify(results),200
        

