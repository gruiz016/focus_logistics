from flask import Flask, request, render_template, redirect, flash, session, jsonify
from models import db, connect_db, User, DistributionCenter, Load, Carrier, LoadData
from forms import LoginForm, SignupForm, DCCarrierForm, LoadForm, UpdateLocationForm, LoadDataForm
from helper import get_user_carriers, get_dc, get_miles
import os
from secret import MAP_QUEST_KEY, MAP_QUEST_SECRET

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///freight_db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'This_is_a_secret!')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['CONSUMER_KEY'] = os.environ.get('CONSUMER_KEY', MAP_QUEST_KEY)
app.config['CONSUMER_SECRET'] = os.environ.get('CONSUMER_SECRET', MAP_QUEST_SECRET)

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

@app.route('/manage', methods=['GET', 'POST'])
def user_portal():
    '''Renders the user portal.'''
    # Checks if user has been autherized prior to allowing entrance to route.
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')
    # Grabs all loads.
    loads = Load.query.all()
    # Sets forms carrier and DC options.
    tup_carriers = get_user_carriers()
    tup_dc = get_dc()
    # Selectfield form values.
    form = LoadForm()
    form.carrier_id.choices = tup_carriers
    form.d_c_id.choices = tup_dc
    if form.validate_on_submit():
        po = form.po.data
        name = form.name.data
        city = form.city.data
        state = form.state.data
        due_date = form.due_date.data
        day_of_week = form.day_of_week.data
        temp = form.temp.data
        team = form.team.data
        carrier_id = form.carrier_id.data
        d_c_id = form.d_c_id.data
        # Calls MapQuest API to get distance
        miles = get_miles(app=app.config['CONSUMER_KEY'], dc_id=d_c_id, city=city, state=state)
        # Creates load object 
        load = Load(po=po, name=name, pickup_city=city, pickup_state=state, due_date=due_date, day_of_week=day_of_week, temp=temp, team=team, miles=miles, carrier_id=carrier_id, d_c_id=d_c_id)
        if load:
            db.session.add(load)
            db.session.commit()
            flash('Load created!', 'alert-success')
            return redirect('/manage')
    return render_template('user/portal.html', form=form, loads=loads)

@app.route('/locations', methods=['GET', 'POST'])
def locations():
    '''Renders and handles DC locations users add.'''
    # Checks if user has been autherized prior to allowing entrance to route.
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')
    
    form = DCCarrierForm()
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

@app.route('/carriers', methods=['GET', 'POST'])
def carriers():
    '''Renders and handles carriers the user adds.'''
    # Checks if user has been autherized prior to allowing entrance to route.
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')
    form = DCCarrierForm()
    # Grabs all the carrier information.
    carriers = Carrier.get_carrier_by_user(user_id=session['user_id'])
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip = form.zip.data
        phone = form.phone.data
        # Creates a carrier.
        carrier = Carrier(name=name, address=address, city=city, state=state, zip=zip, phone=phone, user_id=session['user_id'])
        # If carrier was created we commit it.
        if carrier:
            db.session.add(carrier)
            db.session.commit()
            flash('Carrier created!', 'alert-success')
            return redirect('/carriers')
    return render_template('user/carriers.html', form=form, carriers=carriers)

@app.route('/update_location/<int:load_id>', methods=['GET', 'POST'])
def update_location(load_id):
    '''Renders and handles updates to load locations.'''
    # Checks if user has been autherized prior to allowing entrance to route.
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')    
    form = UpdateLocationForm()
    load = Load.query.filter_by(id=load_id).first()
    if form.validate_on_submit():
        load.pickup_city = form.city.data
        load.pickup_state = form.state.data
        load.miles = get_miles(app=app.config['CONSUMER_KEY'], dc_id=load.d_c_id, city=load.pickup_city, state=load.pickup_state)
        # Commits changes.
        db.session.commit()
        flash('Load updated', 'alert-success')
        return redirect('/manage')
    return render_template('user/update.html', form=form)

@app.route('/add_data/<int:load_id>', methods=['GET', 'POST'])
def add_load_data(load_id):
    '''Renders and handles adding load data for each load.'''
    # Checks if user has been autherized prior to allowing entrance to route.
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')    
    form = LoadDataForm()
    if form.validate_on_submit():
        ontime = form.ontime.data
        damges = form.damages.data
        breakdown = form.breakdown.data
        cost = form.cost.data
        pallets = form.pallets.data
        weight = form.weight.data
        # Creates load data object
        data = LoadData(load_id=load_id, user_id=session['user_id'], ontime=ontime, damges=damges, breakdown=breakdown, cost=cost, pallets=pallets, weight=weight)
        # Confirms object was created before we commit.
        if data:
            db.session.add(data)
            db.session.commit()
            flash('Load Data added.', 'alert-success')
            return redirect('/manage')
    return render_template('user/load_data.html', form=form)
