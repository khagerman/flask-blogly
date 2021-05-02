"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "dogsarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def list_users():
    """redirect to list of all users from homepage"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """Shows list of all users in db"""
    user = User.query.all()
    return render_template("list.html", users=users)


@app.route("/users/new", methods=["POST"])
def create_user():
    """Create a new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img = request.form["img"]

    new_user = User(first_name=first_name, last_name=last_name, img_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/{new_user.id}")


@app.route("/<int:id>")
def show_user_details(id):
    """Show details about a single user"""
    pet = Pet.query.get_or_404(user_id)
    return render_template("details.html", pet=pet)
