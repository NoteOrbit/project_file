from pymongo import MongoClient
from flask import Flask, request
from flask_jwt_extended import JWTManager
import datetime
from flask_cors import CORS
from blueprints import *
from extensions import scheduler
from config import client
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():

    app = Flask(__name__)

    setup_db = client['system']
    setup_model = setup_db['model_log']
    db = client['system']
    model_cf = setup_model.find(
        {"model_name": "SVD"}, {"path": 1, '_id': 0}).sort([("_id", -1)]).limit(1)
    setup_model_cf = [x for x in model_cf]
    app.config['path'] = setup_model_cf[0]['path']

    CORS(app, origins='*',supports_credentials=True)
    jwt = JWTManager(app)  # initialize JWTManager
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)
    app.config['SCHEDULER_API_ENABLED'] = True
    jwt.init_app(app)
    app.register_blueprint(recom_near)
    app.register_blueprint(recommend_rule)
    app.register_blueprint(Reg)
    app.register_blueprint(login1)
    app.register_blueprint(log_system)
    app.register_blueprint(general)

    @app.before_request
    def before_request():
        x = request.url
        print(x.split('/')[3])
        db.logs.insert_one({"timestamp": datetime.datetime.now(
        ), "method": request.method, "endpoint": request.url})
    return app



app = create_app()


if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True,host='0.0.0.0',port=5001)
