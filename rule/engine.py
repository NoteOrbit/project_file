import numpy as np
import pickle

# Load the model from the file
with open('age_gender_rules1.pkl', 'rb') as f:
    age_gender_rules = pickle.load(f)


# Implement the recommender system
def recommend(user_age_group, user_gender):
    recommended_items = set()
    rules = age_gender_rules[(user_age_group, user_gender)]
    for index, row in rules.nlargest(10, 'confidence').iterrows():
        recommended_items.add(row["consequents"])
    return list(recommended_items)

gender = input('Gender: ')
z = lambda x: '10-20' if x <= 20 else '21-40' if x <= 40 else '41-60' if x <= 60 else '60+'
age = z(int(input('Age: ')))
print(recommend(age, gender))