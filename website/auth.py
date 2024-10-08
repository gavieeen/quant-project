from flask import Blueprint, render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import pyscrypt
from flask_login import login_user, login_required, logout_user,current_user
auth = Blueprint('auth',__name__)

@auth.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        if user:
            if user.password == password:
                flash("Logged in successfully!", category="success")
                # Redirect to the home page or wherever you need
                login_user(user, remember = True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error") 
        else:
            flash("Email does not exist", category="error")
    return render_template("login.html" , user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

def hash_password(password):
    salt = b"random_salt"
    N = 16384
    r = 8
    p = 1
    dk_len = 64
    return pyscrypt.hash(password.encode('utf-8'), salt, N, r, p, dk_len)
def check_password(stored_password_hash, provided_password):
    salt = b"random_salt"  # Retrieve the actual salt used for the stored password
    N = 16384
    r = 8
    p = 1
    dk_len = 64
    return stored_password_hash == pyscrypt.hash(provided_password.encode('utf-8'), salt, N, r, p, dk_len)
@auth.route('/sign-up', methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category = "error")
        elif len(first_name) < 2:
            flash("First name must be greater than 2 characters.", category = "error")
        elif password1 != password2:
            flash("Passwords do not match.", category = "error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category = "error")
        else:
            #add user to database
            new_user = User(email = email, first_name = first_name, password = password1)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category = "success")
            return redirect(url_for("views.home"))
    return render_template("sign_up.html",user = current_user)