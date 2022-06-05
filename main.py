from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
import os

ENGINE_AWS = 'aws'
ENGINE_AZURE = 'azure'
ENGINES = (
    (ENGINE_AWS, 'AWS'),
    (ENGINE_AZURE, 'Azure')
)

LANG_ES = 'es'
LANG_EN = 'en'
LANGS = (
    (LANG_ES, 'ES'),
    (LANG_EN, 'EN')
)

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
from src.entity import image_to_text
image_to_text.init()

# Import services
from src.service import google_login
google_login.init(app)
from src.service import user_manager
user_manager.init(app)
from src.service import aws_service
aws_service.init(app)
from src.service import azure_service
azure_service.init(app)

# Import controllers
from src.controller import homepage
app.register_blueprint(homepage.mod)
from src.controller import dashboard
app.register_blueprint(dashboard.mod)
from src.controller import text_to_speech
app.register_blueprint(text_to_speech.mod)
from src.controller import speech_to_text
app.register_blueprint(speech_to_text.mod)
from src.controller import image_to_text
app.register_blueprint(image_to_text.mod)

# Configure jinja global variables
app.jinja_env.globals.update(aws_service=aws_service)


@app.errorhandler(404)
def error_not_found():
    return '<p>404 Not found</p>'


@app.errorhandler(500)
def error_internal_server_error():
    return '<p>500 Internal Server Error</p>'

# db.create_all()
