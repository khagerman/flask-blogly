"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "dogsarecool21837"

debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()


@app.route("/")
def home():
    """redirect to list of all users from homepage"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template("/users/index.html", users=users)


@app.route("/users/new", methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template("users/new.html")


@app.route("/users/new", methods=["POST"])
def create_user():
    """Create a new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:id>")
def show_user_details(id):
    """Show details about a single user"""
    user = User.query.get_or_404(id)
    return render_template("details.html", user=user)


@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    """delete user from db"""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:id>/edit", methods=["GET"])
def edit_page(id):
    """edit user in db"""
    user = User.query.get_or_404(id)

    return render_template("users/edit.html", user=user)


@app.route("/users/<int:id>/edit", methods=["POST"])
def edit_user(id):
    """edit user in db"""
    user = User.query.get_or_404(id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.add(user)
    db.session.commit()

    return redirect("/users")
