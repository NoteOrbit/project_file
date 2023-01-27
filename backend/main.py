from flask import Flask
from pymongo import MongoClient
import hashlib
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import datetime
import hashlib
import urllib
from flask_cors import CORS
from blueprints import *
from extensions import scheduler

client = MongoClient('localhost', 27017)
db = client['system']
users_collection = db['user']
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


# cors = CORS(app, resources={r"/*":{
#     'origins':"*",
#     'methods':['OPTIONS',"GET","POST","PUT"]
    
# }
# })

jwt = JWTManager(app) # initialize JWTManager
app.config['JWT_SECRET_KEY'] = '38dd56f56d405e02ec0ba4be4607eaab'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt.init_app(app)
scheduler.init_app(app)
scheduler.start()

# app.register_blueprint(home_page)
# app.register_blueprint(location_page)


app.register_blueprint(recom_near)
app.register_blueprint(recommend_rule)
app.register_blueprint(Reg)
app.register_blueprint(login1)
app.register_blueprint(log_system)
app.register_blueprint(general)

@app.before_request
def before_request():
    db.logs.insert_one({"timestamp": datetime.datetime.now(), "method": request.method, "endpoint": request.url})



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")