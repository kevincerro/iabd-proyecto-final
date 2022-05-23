from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.errorhandler(404)
def error_not_found(e):
    return '<p>404 Not found</p>'


@app.errorhandler(500)
def error_not_found(e):
    return '<p>500 Internal Server Error</p>'
