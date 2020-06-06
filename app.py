from flask import Flask, request, render_template, redirect, flash, session, jsonify
from models import db, connect_db, User, DistributionCenter, Load, Carrier, LoadData
from forms import LoginForm, SignupForm, DistributionCenterForm
from helper import check_if_logged_in
import requests
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///freight_db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'This_is_a_secret!')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# 
# LANDING PAGE
# 

@app.route('/')
def home():
    '''Renders home screen or user's manage page.'''
    # Checks if user id in session and directs accordingly!
    if 'user_id' in session:
        return redirect('/manage')
    return render_template('home.html')

# 
# Login, SignUp, and Logout views
# 

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Renders and handles the login.'''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Checks user credentials
        user = User.authenticate(username=username, password=password)
        # If user is authenticated we set users session.
        if user:
            session['user_id'] = user.id
            flash(f'Welcome back {username}!', 'alert-success')
            return redirect('/manage')
        else:
            flash('Username/Password is incorrect.', 'alert-danger')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Renders and handles the signup.'''
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Signs user up
        user = User.singup(username=username, password=password)
        # Verifies if user was created before commiting to database
        if user:
            session['user_id'] = user.id
            db.session.add(user)
            db.session.commit()
            flash(f'{username} was created!', 'alert-success')
            return redirect('/manage')
    return render_template('signup.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    '''Handles logging out a user.'''
    session.pop('user_id')
    flash("You've been logged out!", 'alert-success')
    return redirect('/')

# 
# USER VIEWS
# 

@app.route('/manage')
def user_portal():
    '''Renders the user portal.'''
    # Checks if user has been autherized prior to allowing entrance to route.
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')
    return render_template('user/portal.html')

@app.route('/locations', methods=['GET', 'POST'])
def locations():
    '''Renders and handles DC locations users add.'''
    # Checks if user has been autherized prior to allowing entrance to route.
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')
    
    form = DistributionCenterForm()
    # Grabs all user DC locations
    dc = DistributionCenter.get_dist_by_user(user_id=session['user_id'])
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip = form.zip.data
        phone = form.phone.data
        # Creates a new DC location
        dc = DistributionCenter(name=name, address=address, city=city, state=state, zip=zip, phone=phone, user_id=session['user_id'])
        # If location was created, we commit.
        if dc:
            db.session.add(dc)
            db.session.commit()
            flash('Location created!', 'alert-success')
            return redirect('/locations')
    return render_template('user/locations.html', form=form, dc=dc)