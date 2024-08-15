from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Please fill in both email and password.", category='danger')

        else:
            user = User.query.filter_by(email=email).first()
            if user: 
                if check_password_hash(user.password, password):
                    flash("Login successful!", category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else: 
                    flash('Incorrect password, try again.', category='danger')
            else:
                flash('User does not exit.', category='danger')
                    
    return render_template('login.html', title='Login', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    flash("You have been logged out successfully.", category='success')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        user = User.query.filter_by(email=email).first()

        if user: 
            flash('Email already exits. Sign up with another email.', category='danger')
        elif len(email) < 4:
            flash("Email must be at least 4 characters long.", category='danger')
        
        elif len(full_name) < 6:
            flash("Full Name must be at least 6 characters long.", category='danger')
        
        elif len(password) < 8:
            flash("Password must be at least 8 characters long.", category='danger')
        
        elif password != confirm_password:
            flash("Passwords do not match. Please ensure both passwords are identical.", category='danger')
        
        else:
            new_user = User(full_name=full_name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            
            db.session.add(new_user)
            db.session.commit()
            print('User Info: ', new_user)

            flash("Your account has been created successfully! Please log in.", category='success')
            return redirect(url_for('auth.login'))

    return render_template('sign-up.html', title='Sign Up', user=current_user)
