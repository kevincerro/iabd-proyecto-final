from main import db
from sqlalchemy import func, ForeignKey


def init():
    pass


class TextToSpeech(db.Model):
    __tablename__ = "TextToSpeech"
    id = db.Column(db.Integer, primary_key=True)
    engine = db.Column(db.String(25), index=False, unique=False, nullable=True)
    lang = db.Column(db.String(25), index=False, unique=False, nullable=True)
    text = db.Column(db.Text(), index=False, unique=False, nullable=False)
    speech = db.Column(db.String(100), index=False, unique=False, nullable=True)
    created_by = db.Column(db.Integer, ForeignKey('Users.id'))
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=False, server_default=func.now())

    def __repr__(self):
        return "<TextToSpeech {}>".format(self.id)
