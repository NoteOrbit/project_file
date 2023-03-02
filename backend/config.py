from pymongo import MongoClient

client = MongoClient("0.0.0.0",
                     port=27018,
                     username='root',
                     password='example',
                     authSource='admin')

