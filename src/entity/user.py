from main import db


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=False, unique=False, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    google_id = db.Column(db.String(255), index=True, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)
