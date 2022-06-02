from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
import os

# Initialize flask
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db = SQLAlchemy(app)

# Initialize session
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_SQLALCHEMY_TABLE'] = 'Sessions'
app.config['PERMANENT_SESSION_LIFETIME'] = 604800  # 7 days
Session(app)

# Import models
from src.entity import user
user.init()
from src.entity import text_to_speech
text_to_speech.init()
from src.entity import speech_to_text
speech_to_text.init()

# Import services
from src.service import google_login
google_login.init(app)
from src.service import user_manager
user_manager.init(app)
from src.service import aws_service
aws_service.init(app)

# Import controllers
from src.controller import homepage
app.register_blueprint(homepage.mod)
from src.controller import dashboard
app.register_blueprint(dashboard.mod)

# Configure jinja global variables
app.jinja_env.globals.update(aws_service=aws_service)


@app.errorhandler(404)
def error_not_found():
    return '<p>404 Not found</p>'


@app.errorhandler(500)
def error_internal_server_error():
    return '<p>500 Internal Server Error</p>'
