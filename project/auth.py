from flask import Blueprint, app, render_template, request,flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from sqlalchemy import text
from .models import User
from . import db, app
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('password') else False
    
    user = User.query.filter_by(email = email).first()
    #checks if user exists
    if not user or not (check_password_hash(user.password, password)): #compares hashed passwords
        flash('Please check your login details and try again.')
        app.logger.warning("User login failed")
        return redirect(url_for('auth.login')) #reloads the page on failed login
    
    #logs in the user if the above condition passes
    login_user(user, remember=remember)
    return redirect(url_for('main.homepage'))

@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    first_name = request.form.get('first name')
    last_name = request.form.get('last name')
    password = request.form.get('password')

    user = db.session.execute(text('select * from user where email = "'+email+'"')).all()
    if user:
        flash('Email address already exists')
        app.logger.warning("User signup failed")
        return redirect(url_for('auth.signup'))
    
    hashed_pass = generate_password_hash(password)
    new_user = User(email=email, last_name = last_name, first_name=first_name, password=hashed_pass)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))