import mongoengine as me

class User(me.Document):
    id = me.IntField(unique=True)
    name = me.StringField()
    email = me.StringField()
    
    