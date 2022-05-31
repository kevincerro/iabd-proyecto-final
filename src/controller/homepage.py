from flask import Blueprint, redirect, url_for, request
from flask_login import current_user, login_user
from src.service import google_login, user_manager

mod = Blueprint('homepage', __name__, url_prefix='/')


@mod.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    else:
        return redirect(url_for('homepage.login'))


@mod.route('/login')
def login():
    return redirect(google_login.login())


@mod.route('/login/callback')
def callback():
    # Process google login callback
    code = request.args.get("code")
    response = google_login.callback(code)

    # Get user from db
    user = user_manager.get_or_create_user(response)
    login_user(user)

    return redirect(url_for('dashboard.index'))
