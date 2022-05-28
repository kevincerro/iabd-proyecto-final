from flask import Blueprint

mod = Blueprint('homepage', __name__, url_prefix='/')


@mod.route('/')
def homepage():
    return '<p>Hello, World!</p>'
