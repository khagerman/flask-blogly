"""Seed file to make sample data for user db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add user
jane = User(first_name="Jane", last_name="Smith")

katherine = User(first_name="Katherine", last_name="Hagerman")

# Add new objects to session, so they'll persist
db.session.add(jane)

db.session.add(katherine)

# Commit--otherwise, this never gets saved!
db.session.commit()
