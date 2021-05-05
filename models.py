"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

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

    image_url = db.Column(db.String(255), default=default_img)
    # posts = db.relationship("Posts")


# class Post(db.Model):
#     """post object"""

#     __tablename__ = "post"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     title = db.Column(db.String(10), nullable=False, unique=False)
#     content = db.Column(db.String(200), nullable=False, unique=False)

#     created_at = db.Column(
#         db.DateTime(timezone=True), default=datetime.datetime.now, nullable=False
#     )
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     user = db.relationship("user")
