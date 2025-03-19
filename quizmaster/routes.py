from flask import render_template, redirect, url_for, flash
from quizmaster import app, db, bcrypt
from .forms import Login, Register
from .models import User
import logging
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied: Admin privileges required.', 'danger')
            return redirect(url_for('hello_world'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def hello_world():
    return render_template('layout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user = User(Full_Name=form.Full_Name.data, Email=form.Email.data, Qualification=form.Qualification.data, Password=hashed_password, dob=form.dob.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = Login()
    if form.validate_on_submit():
        logging.debug('Form validated successfully')
        user = User.query.filter_by(Email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.Password.data):
            logging.debug('User found and password matched')
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('hello_world'))
        else:
            logging.debug('Login failed: Invalid email or password')
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        logging.debug('Form validation failed')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!','success')
    return redirect(url_for('hello_world'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')
