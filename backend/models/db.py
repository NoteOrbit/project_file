from pymongo import MongoClient 

db = MongoClient()

def init_db(app):
    db.init_app(app)
