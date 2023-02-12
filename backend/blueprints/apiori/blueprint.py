import pickle
from flask import Blueprint, request, jsonify , current_app
import json
from pymongo import MongoClient
import pandas  as pd
import numpy as np
import hashlib
from scipy.sparse.linalg import svds
from datetime import datetime
from extensions import scheduler
import sys
from bson import json_util
from config import client
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pprint
recommend_rule = Blueprint('recommend_rule', __name__)
# client = MongoClient('mongodb://0.tcp.ap.ngrok.io:17474', 27017)
setup_db = client['system']
setup_model = setup_db['model_log']
model_cf = setup_model.find({"model_name": "CF"}, {"path": 1, '_id': 0}).sort([("_id", -1)]).limit(1)

setup_model_cf = [x for x in model_cf]
sys.path.append("...")
# current_app.config['setup_cf'] = setup_model_cf[0]['path']
# print(current_app.config['setup_cf'])
current_model = None
global path_current
path_current = setup_model_cf[0]['path']
print(path_current)
with open(setup_model_cf[0]['path'], 'rb') as f:
    current_model = pickle.load(f)

class CFRecommender2:
    
    MODEL_NAME = 'Collaborative Filtering'
    
    def __init__(self, cf_predictions_df, projects_df=None):
        self.cf_predictions_df = cf_predictions_df
        self.projects_df = projects_df
        
    def get_model_name(self):
        return self.MODEL_NAME
        
    def recommend_projects(self, donor_id, projects_to_ignore=[], topn=10):
        # Get and sort the donor's predictions
        sorted_donor_predictions = self.cf_predictions_df[donor_id].sort_values(ascending=False) \
                                    .reset_index().rename(columns={donor_id: 'recStrength'})
        
        # Recommend the highest predicted projects that the donor hasn't donated to
        recommendations_df = sorted_donor_predictions[~sorted_donor_predictions['Store'].isin(projects_to_ignore)] \
                               .sort_values('recStrength', ascending = False) \
                               .head(topn)

        return recommendations_df
    
@recommend_rule.route('/getmodel',methods=['GET'])
def get_models():
    db = client['system']
    model_collection = db['model_log']
    models = model_collection.find({}, ).sort("date", -1)
    models = list(models)
    for model in models:
        model["_id"] = str(model["_id"])
    return jsonify(models),200


@recommend_rule.route('/get_current',methods=['GET'])
def current_model1():
    js = {
        "model_cf":current_app.config['path']
    }

    return jsonify(js)


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
    path_current = selected_model_path
    current_app.config['path'] = path_current
    print(current_app.config['path'])

    return jsonify({'message': 'Model successfully switched'},200)


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


    mse = np.mean((user_df.values - predicted_ratings)**2)
    mse = np.round(mse, 4)

    systempath = client['system']
    model = systempath['model_log']
    js = {
        "model_name":"CF",
        "path":f"model/CF/{filename}",
        "date":datetime.now(),
        "setting":{"K":values},
        "measures":{"mse":mse,
                    }
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

@recommend_rule.route('/save_as', methods=['POST'])
def savemodelsa():
    _json = request.json
    support_values = int(_json['sup'])
    metric = _json['metric']
    confidence_values = int(_json['con'])
    base_on = _json['base_on'] 
    pipeline = [
        {
            '$lookup': {
                'from': "Transactions",
                'localField': "uid",
                'foreignField': "uid",
                'as': "combined_documents"
            }
        },
        {
            '$match': { 'combined_documents.event': base_on }
        },
        {
            '$unwind': "$combined_documents"
        },
        {
            '$match': { 'combined_documents.event': base_on }
        },
        {
            '$group': {
                '_id': "$_id",
                'name': { '$first': "$name" },
                'Gender': { '$first': "$gender" },
                'Age': { '$first': "$age" },
                'Store': {
                    '$addToSet': "$combined_documents.Content"
                }
            }
        }
    ]

    """
    
    setup db for retrain asscations rule

    """
    if support_values and metric and confidence_values and base_on:
        db = client['Infomations']
        collections = db['User']
        data = list(collections.aggregate(pipeline)) ## pipeline data
        df1 = pd.DataFrame(data) ## Create table for retraining
        df1 = df1.iloc[0:,[3,2,4]] ## remove coulume not use
        df1["Gender"] = df1["Gender"].apply(lambda x:x.lower())  ## setup lower case text

        """
        setup  load previous data
        
        """
        
        old_data = pd.read_csv("data/Form.csv")
        old_data = old_data.iloc[0:,[1,2,3]] ## remove coulume not use
        old_data['Store'] = old_data['Store'].apply(lambda x: x.split(","))
        print(old_data)
        old_data = old_data.append(df1,ignore_index=True) ## append data to previouse data
        
        old_data['age_group'] = old_data['Age'].apply(lambda x: '10-20' if x <= 20 else '21-40' if x <= 40 else '41-60' if x <= 60 else '60+')

        age_groups = old_data.groupby('age_group')
        age_gender_rules = {}

        # Run the Apriori algorithm and generate association rules for each age group and gender
        try:
            for age_group, data in age_groups:
                for gender, gender_data in data.groupby('Gender'):
                    # Use the TransactionEncoder to convert the data into a suitable format for the Apriori algorithm
                    te = TransactionEncoder()
                    te_ary = te.fit(gender_data['Store']).transform(gender_data['Store'])
                    df_temp = pd.DataFrame(te_ary, columns=te.columns_)

                    # Run the Apriori algorithm to find frequent item sets
                    frequent_itemsets = apriori(df_temp, min_support=support_values/100, use_colnames=True)

                    # Generate association rules from the frequent item sets
                    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=confidence_values/100)
                    # Store the association rules for each age group and gender in the dictionary
                    age_gender_rules[(age_group, gender)] = rules

            now = datetime.now()
            filename = "association" + now.strftime("%Y_%m_%d_%H_%M_%S") + ".pkl"
            with open('model/apiori/'+filename, 'wb') as f:
                pickle.dump(age_gender_rules, f)
                systempath = client['system']
            model = systempath['model_log']
            js = {
                "model_name":"association_rule",
                "path":f"model/apiori/{filename}",
                "date":datetime.now(),
                "setting":{"metric":metric,
                           "support":support_values,
                           "confidence":confidence_values,
                           "baseon":base_on
                           },
            }
            model.insert_one(js)
            return jsonify({"msg":"Train"}),201
        except:
            return jsonify({"msg":"error"}),400
    else:
        return jsonify({"msg":"no key"}),400


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
        preds_df_1 = current_model ## set up model
        print(preds_df_1)
        data = users_collection.find({}, {'Store':1, '_id':0,'User':1,'Rating':1})
        df11 =  pd.DataFrame(list(data))

        user_df = df11.pivot_table(index="User",columns="Store",values='Rating').fillna(0)

        hh = CFRecommender2(preds_df_1,user_df)
        sss = user_df.loc[user_name]
        indexes = sss[sss > 0].index

        data2 = hh.recommend_projects(user_name,indexes)
        json2 = data2['Store']
        lista = [x for x in json2]
        print(lista)
        pipeline = [
            {"$match": {"store": {"$in": lista}}},
            {"$addFields": { "index": { "$indexOfArray": [ lista, "$store" ] } } },
            {"$sort": {"index": 1}},
            {"$project": {"_id":0}}
        ]
        store = db['new_collection']
        results = list(store.aggregate(pipeline))
        results.append(current_app.config['path'])
        messs = {
            "data":results,
            "model":"SVDS"
        }
        s = json.dumps(messs)
        b = json.loads(s)


        log = client['system']
        log_system = log['recommendations']
        hash_object = hashlib.sha256(current_app.config['path'].encode())
        hex_dig = hash_object.hexdigest()
        data_log = {
            "recommend_id":hex_dig,
            "uid":user_name,
            "recommend_item":lista,
            "path_model":current_app.config['path'],
            "date":datetime.now()
            }

        check_user = log_system.find_one({"uid":user_name,"recommend_id":hex_dig})
        if not check_user:
             log_system.insert_one(data_log)
        else:
             pass

        return jsonify(b), 200
    else:
        users_collection = db['User']
        user_check = users_collection.find({'uid': user_name},{"gender":1,"age":1,"_id":0})
        user = {}
        
        for x in user_check:
            user = x

        mapage = lambda x: '10-20' if x <= 20 else '21-40' if x <= 40 else '41-60' if x <= 60 else '60+'
        user['age'] = mapage(user['age'])
        user['gender'] = user['gender'].lower()
        with open('model/apiori/association2023_02_11_19_44_01.pkl', 'rb') as f:
            age_rule = pickle.load(f)

        rules = age_rule[(user['age'], user['gender'].lower())].sort_values(by='confidence', ascending=False)


        recommended_items = set()
        for index, row in rules.head(15).iterrows():
            recommended_items.add(row["consequents"])
        recommended_items = list(recommended_items)
        recommended_items = [list(item) for item in recommended_items]
        re = set()
        for a in recommended_items:
            da = set([ss.strip() for ss in a])
            re.update(da)
        lista = list(re)
        print(lista)
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
            "model":"association rule"
        }
        s = json.dumps(messs)
        b = json.loads(s)

        return jsonify(b)
    

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

