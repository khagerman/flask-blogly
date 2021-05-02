"""Seed file to make sample data for user db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Pet.query.delete()

# Add user
jane = User(first_name="Jane", last_name="Smith")
bob = User(
    first_name="Bob",
    last_name="Ross",
    img="https://yt3.ggpht.com/ytc/AAUvwnhkZjfj3AhZNOvbxzIzVLTKZZHGLAlIHVstuYx1=s900-c-k-c0x00ffffff-no-rj",
)
katherine = User(first_name="Katherine", last_name="Hagerman")

# Add new objects to session, so they'll persist
db.session.add(jane)
db.session.add(bob)
db.session.add(katherine)

# Commit--otherwise, this never gets saved!
db.session.commit()
