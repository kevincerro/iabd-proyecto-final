from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Import models
from src.entity import user
user.init()

# Import services
from src.service import google_login
google_login.init(app)
from src.service import user_manager
user_manager.init(app)
# Import controllers
from src.controller import homepage
app.register_blueprint(homepage.mod)


@app.errorhandler(404)
def error_not_found(e):
    return '<p>404 Not found</p>'


@app.errorhandler(500)
def error_not_found(e):
    return '<p>500 Internal Server Error</p>'
