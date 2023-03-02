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
