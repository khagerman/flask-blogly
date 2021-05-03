"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_img = "https://justmarkup.com/img/avatar-default.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
    """user"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)

    image_url = db.Column(db.String(500), default=default_img)
