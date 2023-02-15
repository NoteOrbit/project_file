from flask import Flask, jsonify, request, Response , render_template ,Blueprint
import requests
import json
from flask_cors import CORS
from flask_pymongo  import PyMongo
from math import radians, sin, cos, sqrt, atan2
from pymongo import MongoClient 
from bson import json_util
from bson.objectid import ObjectId
from functools import wraps
from datetime import datetime
from flask_bcrypt import Bcrypt
import jwt
from pymongo.client_session import ClientSession
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = 'mysecretkey'
bcrypt = Bcrypt(app)
secret = "***************"
client = MongoClient('localhost', 27017)
CORS(app)


def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                jwt.decode(token, secret)
            except:
                return jsonify({"status": "fail", "message": "unauthorized"}), 401
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "fail", "message": "unauthorized"}), 401
    return decorated


#load model apiori
with open('age_gender_rules1.pkl', 'rb') as f:
    age_gender_rules = pickle.load(f)
    

@app.route('/signup', methods=['POST'])
def save_user():
    db = client['Infomations']
    message = ""
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        check = db['User'].find({"email": data['email']})
        if check.count() >= 1:
            message = "user with that email exists"
            code = 401
            status = "fail"
        else:
            # hashing the password so it's not stored in the db as it was 
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['created'] = datetime.now()

            #this is bad practice since the data is not being checked before insert
            res = db["User"].insert_one(data) 
            if res.acknowledged:
                status = "successful"
                message = "user created successfully"
                code = 201
    except Exception as ex:
        message = f"{ex}"
        status = "fail"
        code = 500
    return jsonify({'status': status, "message": message}), 200


## save log call functions
def log_call(func):
    @wraps(func) ## decorator functions
    def wrapper(*args, **kwargs):
        db = client['log_service']
        logs = db['log_system']
        logs.insert_one({
            'timestamp': datetime.utcnow(),
            'function': func.__name__
        })
        return func(*args, **kwargs)
    return wrapper


## web sections
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/webnearby', methods=['GET'])
def nearbyweb():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    info = requests.get(f'http://127.0.0.1:5000/nearby?latitude={latitude}&longitude={longitude}')
    posts=info.json()
    return render_template('nearby.html', posts=posts)

@app.route('/showstore', methods=['GET'])
def filterweb():
    db = client['Infomations']
    collections = db['new_collection']
    liststore = collections.find({},{'_id':0})
    response = json_util.dumps(liststore)
    posts = json_util.loads(response)
        
    return render_template('showstore.html',posts=posts)


@app.route('/document_api')
def webdoc():
    return render_template('document_api.html')


@app.route('/showrecom')
def webrecom():
    select1 = request.args.get('select2')
    select2 = request.args.get('select1')
    data = {
    "age_group": select1,
    "gender": select2
}

    headers = {"Content-Type": "application/json"}
    info = requests.post("http://127.0.0.1:5000/recom", json=data, headers=headers)
    posts = info.json()
    if 'recommendations' in posts:
        return render_template('Apiori.html',posts=posts['recommendations'])
    else:
        return render_template('Apiori.html',posts=posts)

## web sections



## API sections
@app.route("/add", methods=['POST'])
@log_call
def Adduser(): ## sample create user
    _json = request.json
    _name = _json['name']
    _token = _json['token']
    _age = _json['age']
    _fav = _json['fav']
    if _name and _token and _age and _fav and request.method == 'POST':
        db = client['Infomations']
        collection = db['User']
        collection.insert_one({'name':_name,'token':_token,'age':_age,'fav':_fav})

        resp = jsonify('user  add successfully')

        resp.status_code = 200

        return resp
    else: 
        resp = jsonify('not successfully')
        resp.status_code = 404
        return resp

@app.route("/nearby", methods=["GET"])
@log_call
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
    for point in collection.find({},{'_id':1,'latitude':1,'longitude':1,'store':1}):
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
    return jsonify(results)
        
@app.route("/type", methods=["GET"])
@log_call
def filterbytype():
    db = client['Infomations']
    collections = db['new_collection']
    if request.method == "GET":
        listtype = request.args.get("type").split(',')
        liststore = collections.find({'type': {'$in':listtype}},{'_id':0})
        response = json_util.dumps(liststore)
        re = json_util.loads(response)
        
        return jsonify(re) 
    else:
        return jsonify({"error": "no method for post"}), 400

@app.route("/recom", methods=["POST"])
@log_call
def recommend():

    # Load the model from the file
    global age_gender_rules
    # Get the user's age group and gender
    user_age_group = request.json['age_group']
    user_gender = request.json['gender']
    
    # Get the association rules for the user's age group and gender
    rules = age_gender_rules.get((user_age_group, user_gender))
    if rules is None:
        return jsonify({'error': 'No rules found for the given age group and gender.'}), 400
    
    # Sort the rules by lift and return the top N rules
    N = request.json.get('N', 5)
    sorted_rules = rules.sort_values(by='lift', ascending=False).head(N)
    recommendations = [list(r) for r in sorted_rules['consequents'].tolist()]
    return jsonify({'recommendations': recommendations})



if __name__ == "__main__":
    app.run(debug=True)