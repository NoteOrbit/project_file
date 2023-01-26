import pickle
from flask import Blueprint, render_template, request, jsonify
import json
from pymongo import MongoClient
import pandas  as pd
import numpy as np
import datetime
from scipy.sparse.linalg import svds
from datetime import datetime
from extensions import scheduler
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

# @recommend_rule.route('/save', methods=['POST'])
@scheduler.task('interval', id='save_model', hours=6)
def save_model():

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
    with open('model/'+filename, 'wb') as f:
        pickle.dump(preds_df, f)
    return "Model Saved"

@recommend_rule.route('/recommend', methods=['GET'])
def recommend():
    ## name user
    user_name = request.json['name']
    client = MongoClient('localhost', 27017)
    
    db = client['Infomations']
    users_collection = db['Transaction_user']
    user_check = users_collection.find_one({'User': user_name})
    if user_check:
        with open('model/preds_df_2023_01_26_01_48_24.pkl', 'rb') as f:
            preds_df_1 = pickle.load(f)
        data = users_collection.find({}, {'Store':1, '_id':0,'User':1,'Rating':1})
        df11 =  pd.DataFrame(list(data))
        user_df = df11.pivot_table(index="User",columns="Store",values='Rating').fillna(0)
        hh = CFRecommender2(preds_df_1,user_df)
        sss = user_df.loc[user_name]
        indexes = sss[sss > 0].index    
        data2 = hh.recommend_projects(user_name,indexes)
        json2 = data2['Store']
        messs = {
            "data":[x for x in json2],
            "previous" : [x for x in indexes]
        }
        sb = json.dumps(messs)
        s = json.loads(sb)

        return jsonify(s), 200
    
@recommend_rule.route('/take', methods=['GET',"POST","UPDATE"])
def take():

    db = client['Infomations']
    _json = request.json
    users_collection = db['User']
    name = _json['name']
    gender = _json['gender']
    age = _json['age']
    uid = _json['uid']

    with open('age_gender_rules1.pkl', 'rb') as f:
        age_gender_rules = pickle.load(f)
    mapage = lambda x: '10-20' if x <= 20 else '21-40' if x <= 40 else '41-60' if x <= 60 else '60+'

    if name and gender and age and uid and request.method == "POST":
        _json = request.json
        doc = users_collection.find_one({"name": _json["name"]})
        if doc:
            return jsonify({'msg': 'exctied'}), 401
        
        users_collection.insert_one(_json)
        age_map = mapage(age)
        rules = age_gender_rules[(age_map, gender)]

    # Sort the rules by lift and return the top N rules

        sorted_rules = rules.sort_values(by='confidence', ascending=False).head(10)
        recommendations = [list(r) for r in sorted_rules['consequents'].tolist()]

        return jsonify({'recommendations': recommendations})
    
    if uid and request.method == "GET":
        doc = users_collection.find({"uid": _json["uid"]})
        age = 0
        gender_map = ""
        for x in doc:
            age = x['age']
            gender_map = x['gender']
        age_map = mapage(age)
        rules = age_gender_rules[(age_map, gender_map)]
    # Sort the rules by lift and return the top N rules
        sorted_rules = rules.sort_values(by='confidence', ascending=False).head(10)
        recommendations = [list(r) for r in sorted_rules['consequents'].tolist()]

        return jsonify({'recommendations': recommendations})
   

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


@recommend_rule.route('/model',methods=['GET'])
def get_model_files():
    model_folder = 'model/'
    files = os.listdir(model_folder)
    return jsonify(files)

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

