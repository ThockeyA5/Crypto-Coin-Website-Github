from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Username = request.form.get('Username')
        password = request.form.get('Password')
        
        user = User.query.filter_by(Username=Username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                user = User.query.filter_by(Username=Username).first()
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Username or Password', category='error')
        else:
            flash('Incorrect Username or Password', category='error')
        
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        Username = request.form.get('Username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(Username=Username).first()
        user2 = User.query.filter_by(email=email).first()
        
        if user:
            flash('Username already exists.', category='error')
        elif user2:
            flash('Email already exists.', category='error')
        elif len(email) < 16:
            flash('Email must be at least 16 characters.', category='error')
        elif len(fullname) < 5:
            flash('Name must be at least 5 characters.', category='error')
        elif len(Username) < 5:
            flash('Username must be at least 5 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email=email, fullname=fullname, Username=Username, password=generate_password_hash(password1, method='sha256'), CoinNum = 0)
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(Username=Username).first()
            login_user(user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user = current_user)