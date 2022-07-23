from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category= 'success')
                login_user(user, remember= True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category= 'error')
        else:
            flash("User does not exist!", category= 'error')
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['Get', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email)
        if user:
            flash('User name already exists! Please choose another name!', category= 'error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters!", category='error')
        elif len(firstName) < 2:
            flash("First Name must be greater than 2 characters!", category='error')
        elif password1 != password2:
            flash("Passwords must be the same!", category='error')
        elif len(password1) < 7:
            flash("Password length must be greater than 7 characters.", category='error')
        else:
            #Add user to database
            new_user = User(email= email, first_name= firstName, password= generate_password_hash(password1, method= 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            login_user(user, remember= True)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html")