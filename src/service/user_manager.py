from flask_login import LoginManager

from main import db
from src.entity.user import User

login_manager = LoginManager()


def init(app):
    login_manager.login_view = 'homepage.index'
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def get_or_create_user(data):
    user = User.query.filter_by(google_id=data['sub']).first()
    if user is None:
        user = User(
            name=data['given_name'],
            email=data['email'],
            google_id=data['sub']
        )
        db.session.add(user)
        db.session.commit()

    return user
