import pickle
from flask import Blueprint, render_template, request, jsonify
import requests
import json
from pymongo import MongoClient
import pandas  as pd
import numpy as np


with open('age_gender_rules1.pkl', 'rb') as f:
    age_gender_rules = pickle.load(f)

recommend_rule = Blueprint('recommend_rule', __name__)

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

@recommend_rule.route('/recommend', methods=['GET'])
def recommend():
    ## name user
    user_name = request.json['name']
    client = MongoClient('localhost', 27017)
    
    db = client['Infomations']
    users_collection = db['Transaction_user']
    user_check = users_collection.find_one({'User': user_name})
    if user_check:
        with open('preds_df.pkl', 'rb') as f:
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
    client = MongoClient('localhost', 27017)
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

@recommend_rule.route('/recommend_populations', methods=['GET'])
def recommend1():
    client = MongoClient('localhost', 27017)
    db = client['Infomations']
    users_collection = db['Transaction_user']

    pipeline =  [
    {"$group":{"_id":"$Store","count":{"$sum":1}}},
                                       
    {"$sort":{"count":-1}}
    ]
    total = users_collection.aggregate(pipeline)
    messs = {
        "data":[x['_id'] for x in total]
    }
    sb = json.dumps(messs)
    s = json.loads(sb)

    return jsonify(s), 200

