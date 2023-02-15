from pymongo import MongoClient

client = MongoClient("mongodb",
                     port=27018,
                     username='root',
                     password='example',
                     authSource='admin')

