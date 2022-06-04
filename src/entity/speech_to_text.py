from main import db
from sqlalchemy import func, ForeignKey


def init():
    pass


class SpeechToText(db.Model):
    __tablename__ = "SpeechToText"
    id = db.Column(db.Integer, primary_key=True)
    speech = db.Column(db.String(100), index=False, unique=False, nullable=True)
    text = db.Column(db.Text(), index=False, unique=False, nullable=False)
    created_by = db.Column(db.Integer, ForeignKey('Users.id'))
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=False, server_default=func.now())

    def __repr__(self):
        return "<SpeechToText {}>".format(self.id)
