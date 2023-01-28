import pickle
from flask import Blueprint, request, jsonify 
import json
from pymongo import MongoClient
import pandas  as pd
import numpy as np
import datetime
from scipy.sparse.linalg import svds
from datetime import datetime
from extensions import scheduler
from apscheduler.triggers.interval import IntervalTrigger
import sys
import os

from bson import json_util
sys.path.append("...")

recommend_rule = Blueprint('recommend_rule', __name__)
client = MongoClient('localhost', 27017)



class CFRecommender2:
    
    MODEL_NAME = 'Collaborative Filtering'
    
    def __init__(self, cf_predictions_df, projects_df=None):
        self.cf_predictions_df = cf_predictions_df
        self.projects_df = projects_df
        
    def get_model_name(self):
        return self.MODEL_NAME
        
    def recommend_projects(self, donor_id, projects_to_ignore=[], topn=20):
        # Get and sort the donor's predictions
        sorted_donor_predictions = self.cf_predictions_df[donor_id].sort_values(ascending=False) \
                                    .reset_index().rename(columns={donor_id: 'recStrength'})
        
        # Recommend the highest predicted projects that the donor hasn't donated to
        recommendations_df = sorted_donor_predictions[~sorted_donor_predictions['Store'].isin(projects_to_ignore)] \
                               .sort_values('recStrength', ascending = False) \
                               .head(topn)

        return recommendations_df
    
@recommend_rule.route('/getmodel')
def get_models():
    db = client['system']
    model_collection = db['model_log']
    models = model_collection.find({}, {"path": 1, "date": 1,"model_name":1}).sort("date", -1)
    models = list(models)
    for model in models:
        model["_id"] = str(model["_id"])
    return jsonify(models)


@recommend_rule.route('/switch_model', methods=['POST'])
def switch_model():
    # get the path of the selected model from the client's request
    selected_model_path = request.json['path']
    
    # use the selected model path to load the appropriate model
    with open(selected_model_path, 'rb') as f:
        model = pickle.load(f)
    
    # update the global variable that stores the current model
    global current_model
    current_model = model
    
    return jsonify({'message': 'Model successfully switched'})



@recommend_rule.route('/save_cf', methods=['POST'])
def save_model():
    _json = request.json
    values = int(_json['values'])
    db = client['Infomations']
    users_collection = db['Transaction_user']
    data = users_collection.find({}, {'Store':1, '_id':0,'User':1,'Rating':1})
    df11 =  pd.DataFrame(list(data))
    user_df = df11.pivot_table(index="User",columns="Store",values='Rating').fillna(0)
    user_ids = list(user_df.index)
    U, sigma, Vt = svds(user_df.values, k = values)
    sigma = np.diag(sigma)
    predicted_ratings = np.dot(np.dot(U, sigma), Vt)
    preds_df = pd.DataFrame(predicted_ratings, 
                           columns = user_df.columns, 
                           index=user_ids).transpose()
    now = datetime.now()
    filename = "preds_df_" + now.strftime("%Y_%m_%d_%H_%M_%S") + ".pkl"
    with open('model/CF/'+filename, 'wb') as f:
        pickle.dump(preds_df, f)
    systempath = client['system']
    model = systempath['model_log']
    js = {
        "model_name":"CF",
        "path":f"model/CF/{filename}",
        "date":datetime.now(),
    }
    model.insert_one(js)

    return jsonify({"msg":"sucesss"}),201

# @scheduler.task('interval', id='save_model1', seconds=30)
def save_model1():

    db = client['Infomations']
    users_collection = db['Transaction_user']
    data = users_collection.find({}, {'Store':1, '_id':0,'User':1,'Rating':1})
    df11 =  pd.DataFrame(list(data))
    user_df = df11.pivot_table(index="User",columns="Store",values='Rating').fillna(0)
    user_ids = list(user_df.index)
    U, sigma, Vt = svds(user_df.values, k = 15)
    sigma = np.diag(sigma)
    predicted_ratings = np.dot(np.dot(U, sigma), Vt)
    preds_df = pd.DataFrame(predicted_ratings, 
                           columns = user_df.columns, 
                           index=user_ids).transpose()
    now = datetime.now()
    filename = "preds_df_" + now.strftime("%Y_%m_%d_%H_%M_%S") + ".pkl"
    with open('model/CF/'+filename, 'wb') as f:
        pickle.dump(preds_df, f)
    systempath = client['system']
    model = systempath['model_log']
    js = {
        "model_name":"CF",
        "path":f"model/CF/{filename}",
        "date":datetime.now(),
    }
    model.insert_one(js)

    return "Hlleow"

scheduler.add_job(id='save_model1', func=save_model1, trigger='interval', hours=6)

@recommend_rule.route('/pause_job', methods=['GET'])
def pause_job():
    scheduler.pause_job('save_model1')
    return jsonify({"msg":"Job Paused"}),200


@recommend_rule.route('/resume_job', methods=['GET'])
def resume_job():
    scheduler.resume_job('save_model1')
    return jsonify({"msg":"Job Resumed"}),200

@recommend_rule.route('/check_job', methods=['GET'])
def check_job():
    job = scheduler.get_job('save_model1')
    if job.next_run_time:
        return jsonify({"msg":"Job is running"}),200
    else:
        return jsonify({"msg":"Job is paused"}),203



@recommend_rule.route('/recommend', methods=['GET'])
def recommend():
    user_name = request.args.get("name")
    db = client['Infomations']
    users_collection = db['Transaction_user']
    user_check = users_collection.find_one({'User': user_name})
    if user_check:
        preds_df_1 = current_model
        data = users_collection.find({}, {'Store':1, '_id':0,'User':1,'Rating':1})
        df11 =  pd.DataFrame(list(data))
        user_df = df11.pivot_table(index="User",columns="Store",values='Rating').fillna(0)
        hh = CFRecommender2(preds_df_1,user_df)
        sss = user_df.loc[user_name]
        indexes = sss[sss > 0].index    
        data2 = hh.recommend_projects(user_name,indexes)
        json2 = data2['Store']
        lista = [x for x in json2]
        pipeline = [
            {"$match": {"store": {"$in": lista}}},
            {"$addFields": { "index": { "$indexOfArray": [ lista, "$store" ] } } },
            {"$sort": {"index": 1}},
            {"$project": {"_id":0}}
        ]
        store = db['new_collection']
        results = list(store.aggregate(pipeline))
        messs = {
            "data":results,
        }
        s = json.dumps(messs)
        b = json.loads(s)
        return jsonify(b), 200
    else:
        users_collection = db['User']
        user_check = users_collection.find({'uid': user_name},{"gender":1,"age":1,"_id":0})
        user = {}
        
        for x in user_check:
            user = x

        mapage = lambda x: '10-20' if x <= 20 else '21-40' if x <= 40 else '41-60' if x <= 60 else '60+'
        user['age'] = mapage(user['age'])

        with open('model/age_gender_rules1.pkl', 'rb') as f:
            age_rule = pickle.load(f)

        rules = age_rule[(user['age'], user['gender'])]
            # Sort the rules by lift and return the top N rules

        sorted_rules = rules.sort_values(by='confidence', ascending=False).head(10)
        recommendations = [list(r) for r in sorted_rules['consequents'].tolist()]

        return jsonify({'recommendations': recommendations})
    

# @recommend_rule.route('/take', methods=['GET',"POST","UPDATE"])
# def take():

#     db = client['Infomations']
#     _json = request.json
#     users_collection = db['User']
#     name = _json['name']
#     gender = _json['gender']
#     age = _json['age']
#     uid = _json['uid']

#     with open('age_gender_rules1.pkl', 'rb') as f:
#         age_gender_rules = pickle.load(f)
#     mapage = lambda x: '10-20' if x <= 20 else '21-40' if x <= 40 else '41-60' if x <= 60 else '60+'

#     if name and gender and age and uid and request.method == "POST":
#         _json = request.json
#         doc = users_collection.find_one({"name": _json["name"]})
#         if doc:
#             return jsonify({'msg': 'exctied'}), 401
        
#         users_collection.insert_one(_json)
#         age_map = mapage(age)
#         rules = age_gender_rules[(age_map, gender)]

#     # Sort the rules by lift and return the top N rules

#         sorted_rules = rules.sort_values(by='confidence', ascending=False).head(10)
#         recommendations = [list(r) for r in sorted_rules['consequents'].tolist()]

#         return jsonify({'recommendations': recommendations})
    
#     if uid and request.method == "GET":
#         doc = users_collection.find({"uid": _json["uid"]})
#         age = 0
#         gender_map = ""
#         for x in doc:
#             age = x['age']
#             gender_map = x['gender']
#         age_map = mapage(age)
#         rules = age_gender_rules[(age_map, gender_map)]
#     # Sort the rules by lift and return the top N rules
#         sorted_rules = rules.sort_values(by='confidence', ascending=False).head(10)
#         recommendations = [list(r) for r in sorted_rules['consequents'].tolist()]

#         return jsonify({'recommendations': recommendations})
   

    # return jsonify({'msg': 'User created successfully'}), 201
    # with open('age_gender_rules1.pkl', 'rb') as f:
    #     age_gender_rules = pickle.load(f)

    # recommend_rule = Blueprint('recommend_rule', __name__)



    # Load the model from the file
    # global age_gender_rules
    # Get the user's age group and gender
    # user_age_group = request.json['age_group']
    # user_gender = request.json['gender']


    # else:
    #     return jsonify(user_name), 400
    # Get the association rules for the user's age group and gender
    # rules = age_gender_rules.get((user_age_group, user_gender))
    # if rules is None:
    #     return jsonify({'error': 'No rules found for the given age group and gender.'}), 400
    
    # # Sort the rules by lift and return the top N rules
    # N = request.json.get('N', 5)
    # sorted_rules = rules.sort_values(by='lift', ascending=False).head(N)
    # recommendations = [list(r) for r in sorted_rules['consequents'].tolist()]

    # return jsonify({'recommendations': recommendations})


@recommend_rule.route('/type',methods=['GET'])
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


@recommend_rule.route('/recommend_populations', methods=['GET'])
def recommend1():
    client = MongoClient('localhost', 27017)
    db = client['Infomations']
    users_collection = db['Transaction_user']

    pipeline =  [
    {
        "$lookup": {
            "from": "new_collection",
            "localField": "Store",
            "foreignField": "store",
            "as": "other_collection_data"
        }
    },
    {
        "$project": {
            "Store": 1,
            "other_collection_data": {
                "$map": {
                    "input": "$other_collection_data",
                    "as": "data",
                    "in": {
                        "Store_name": "$$data.store",
                        "addr": "$$data.address	",
                        "rating":"$$data.rating",
                        "count_rating":"$$data.count_rating",
                    }
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$Store",
            "count": {"$sum": 1},
            "other_data": {"$first": "$other_collection_data"}
        }
    },
    {"$sort": {"count": -1}}
]
    total = users_collection.aggregate(pipeline)
    ss = [x['other_data'][0] for x in total]
    messs = {
        "data":ss
    }
    sb = json.dumps(messs)
    s = json.loads(sb)

    return jsonify(s), 200

