from main import db
from sqlalchemy import func, ForeignKey


def init():
    pass


class ImageAnalysis(db.Model):
    __tablename__ = "ImageAnalysis"
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(25), index=False, unique=False, nullable=True)
    image = db.Column(db.String(100), index=False, unique=False, nullable=True)
    text = db.Column(db.String(255), index=False, unique=False, nullable=False)
    created_by = db.Column(db.Integer, ForeignKey('Users.id'))
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=False, server_default=func.now())

    def __repr__(self):
        return "<ImageAnalysis {}>".format(self.id)
