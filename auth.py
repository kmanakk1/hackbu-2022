from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from initialize import db

auth = Blueprint('auth', __name__)

# login page
@auth.route('/login', methods=['GET'])
def login():
    if(request.method == 'GET'):
        return render_template("login.html")

# signup page
@auth.route('/signup', methods=['GET'])
def signup():
    if(request.method == 'GET'):
        return render_template("signup.html")
    else:
        email = request.form.get("email")
        password = request.form.get("pass")
        name = request.form.get("name")

        # check if email already exists
        emailCheck = User.query.filter_by(email=email).first()
        if emailCheck:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # create new user
        newUser = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(newUser)
        db.session.commit()

        # redirect to login page
        return redirect(url_for('auth.login'))

# logout page
@auth.route('/logout')
def logout():
    return 'logout'