from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect('/user_page')

@app.route('/login', methods=["POST"])
def login():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("Invalid email/password.")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid email/password.")
        return redirect('/')
    session["user_id"] = user_in_db.id
    return redirect('/user_page')

@app.route('/user_page')
def show():
    if not session.get("user_id"):
        return redirect ('/')
    data = {
        "id" : session["user_id"]
    }
    logged_in_user = User.get_one(data)
    return render_template("user_page.html", user = logged_in_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')