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
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


class Post(db.Model):
    """post object"""

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(20), nullable=False, unique=False)
    content = db.Column(db.String(250), nullable=False, unique=False)

    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.now, nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Tag(db.Model):
    """tag object"""

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(20), nullable=False, unique=True)
    posts = db.relationship("Post", secondary="post_tags", backref="tags")


class PostTag(db.Model):
    """tag post"""

    __tablename__ = "post_tags"
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
