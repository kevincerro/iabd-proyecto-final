from flask_login import UserMixin
from main import db
from sqlalchemy import func, ForeignKey


def init():
    pass


class TextToSpeech(db.Model):
    __tablename__ = "TextToSpeech"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=False, unique=False, nullable=False)
    text = db.Column(db.String(255), index=False, unique=False, nullable=False)
    speech = db.Column(db.String(255), index=False, unique=False, nullable=True)
    created_by = db.Column(db.Integer, ForeignKey('Users.id'))
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=False, server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.google_id)

    @property
    def is_active(self):
        return self.enabled
