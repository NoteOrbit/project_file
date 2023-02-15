import csv
from pymongo import MongoClient
# from config import client
# Connect to the MongoDB server
# Get the database and collection


client = MongoClient('mongodb://root:example@localhost:27018/?authMechanism=DEFAULT',27018)
db = client['Infomations']
new_collection = db.new_collection

# Open the CSV file
with open('data/infomations_store.csv', encoding="utf-8-sig") as csvfile:
    # Read the CSV file
    reader = csv.DictReader(csvfile)
    # Iterate through each row
    for row in reader:
        # Split string to array
        row['type'] = row['type'].split(',')
        row['rating'] = float(row['rating'])
        row['latitude'] = float(row['latitude'])
        row['longitude'] = float(row['longitude'])
        row['count_rating'] = float(row['count_rating'])
        # Insert the row into the collection
        new_collection.insert_one(row)

