from flask_login import UserMixin
from sqlalchemy.orm import relationship

from main import db
from sqlalchemy import func


def init():
    pass


class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=False, unique=False, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    google_id = db.Column(db.String(255), index=True, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, index=False, unique=False, nullable=False, server_default='0')
    enabled = db.Column(db.Boolean, index=False, unique=False, nullable=False, server_default='1')
    text_to_speech = relationship('TextToSpeech')
    speech_to_text = relationship('SpeechToText')
    image_to_text = relationship('ImageToText')
    image_analysis = relationship('ImageAnalysis')
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, index=False, unique=False, nullable=False, server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.id)

    @property
    def is_active(self):
        return self.enabled
