from flask import Blueprint, redirect, url_for, request
from flask_login import current_user
from src.service import google_login

mod = Blueprint('homepage', __name__, url_prefix='/')


@mod.route('/')
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('homepage.login'))


@mod.route('/login')
def login():
    return redirect(google_login.login())


@mod.route('/login/callback')
def callback():
    code = request.args.get("code")
    response = google_login.callback(code)
    print(response)

    return '<p>todo</p>'
