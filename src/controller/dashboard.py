from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user

mod = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod.route('/')
@login_required
def index():
    return redirect(url_for('dashboard_text_to_speech.list_action'))


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage.index'))
