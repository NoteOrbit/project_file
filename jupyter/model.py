import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pickle


def setlist(x):
    return x.split(',')

file = pd.read_csv('data/Form.csv',index_col=0).reset_index()
file = file.iloc[0:,[1,2,3]]
file['age_group'] = file['Age'].apply(lambda x: '10-20' if x <= 20 else '21-40' if x <= 40 else '41-60' if x <= 60 else '60+')
file['Store'] = file['Store'].apply(setlist)
age_groups = file.groupby('age_group')
age_gender_rules = {}

# Run the Apriori algorithm and generate association rules for each age group and gender
for age_group, data in age_groups:
    for gender, gender_data in data.groupby('Gender'):
        # Use the TransactionEncoder to convert the data into a suitable format for the Apriori algorithm
        te = TransactionEncoder()
        te_ary = te.fit(gender_data['Store']).transform(gender_data['Store'])
        df_temp = pd.DataFrame(te_ary, columns=te.columns_)

        # Run the Apriori algorithm to find frequent item sets
        frequent_itemsets = apriori(df_temp, min_support=0.05, use_colnames=True)

        # Generate association rules from the frequent item sets
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
        # Store the association rules for each age group and gender in the dictionary
        age_gender_rules[(age_group, gender)] = rules

with open('age_gender_rules1.pkl', 'wb') as f:
    pickle.dump(age_gender_rules, f)


