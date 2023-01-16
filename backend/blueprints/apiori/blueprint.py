import pickle
from flask import Blueprint, render_template, request, jsonify
import requests
import json


with open('age_gender_rules1.pkl', 'rb') as f:
    age_gender_rules = pickle.load(f)

recommend_rule = Blueprint('recommend_rule', __name__)


@recommend_rule.route('/recommend_rule', methods=['GET'])
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
