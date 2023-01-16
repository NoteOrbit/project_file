from flask import Flask

from blueprints import *

app = Flask(__name__)
app.secret_key = 'Project'

app.register_blueprint(home_page)
app.register_blueprint(location_page)
app.register_blueprint(recom_near)
app.register_blueprint(recommend_rule)
app.register_blueprint(doc_page) 

if __name__ == '__main__':
    app.run(debug=True)