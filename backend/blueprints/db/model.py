from flask_mongoengine import MongoEngine

db = MongoEngine()

db_config = {
    "db": "mydatabase",
    "host": "mongodb://localhost:27017",
    "alias": "default",
}

db = MongoEngine(config=db_config)


class User(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True)