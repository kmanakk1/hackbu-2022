from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from initialize import db

auth = Blueprint('auth', __name__)

# login page
@auth.route('/signin', methods=['GET', 'POST'])
def login():
    if(request.method == 'GET'):
        return render_template("signin.html")
    else:
        email = request.form.get("email").lower()
        password = request.form.get("password")
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid login')
            return redirect(url_for('auth.login'))
        elif not check_password_hash(user.password, password):
            flash('Invalid login')
            return redirect(url_for('auth.login'))
        
        # log user in
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))

# signup page
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if(request.method == 'GET'):
        return render_template("signup.html")
    else:
        email = request.form.get("email").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        # check if email already exists
        emailCheck = User.query.filter_by(email=email).first()
        if emailCheck:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        if password != confirm_password:
            flash('Passwords don\'t match')
            return redirect(url_for('auth.signup'))
        # create new user
        newUser = User(email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(newUser)
        db.session.commit()

        # redirect to login page
        return redirect(url_for('auth.login'))

# logout page
@auth.route('/logout')
def logout():
    return 'logout'