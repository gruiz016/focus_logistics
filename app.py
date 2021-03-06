from flask import Flask, request, render_template, redirect, flash, session, jsonify
from models import db, connect_db, User, DistributionCenter, Load, Carrier, LoadData
from forms import LoginForm, SignupForm, DCCarrierForm, LoadForm, UpdateLocationForm, LoadDataForm
from helper import get_user_carriers, get_dc, get_miles, ontime_KPI, damages_KPI, breakdown_KPI, avg_cost_load, cost_per_pallet, cost_per_lbs, try_commit, try_commit_rollback, try_signup
import os
# from secret import MAP_QUEST_KEY, MAP_QUEST_SECRET

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///freight_db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'This_is_a_secret!')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['CONSUMER_KEY'] = os.environ.get('CONSUMER_KEY')
app.config['CONSUMER_SECRET'] = os.environ.get('CONSUMER_SECRET')

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
            db.session.add(user)
            return try_signup(id=user.id, success='User was created!', fail='Something went wrong, please try again later. If this continues please email meet.gio@icloud.com.', route='/', duplicate='You already have an account. Please login!')
    return render_template('signup.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    '''Handles logging out a user.'''
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')
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
    loads = Load.query.filter(Load.delivered==0, Load.user_id==session['user_id']).all()
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
        load = Load(po=po, name=name, pickup_city=city, pickup_state=state, due_date=due_date, day_of_week=day_of_week, temp=temp, team=team, miles=miles, carrier_id=carrier_id, d_c_id=d_c_id, user_id=session['user_id'])
        if load:
            try:
                db.session.add(load)
                db.session.commit()
                # After the load has been commited we create the load data so that a user can add/edit from one route.
                data = LoadData(load_id=load.id, user_id=session['user_id'])
                db.session.add(data)
                db.session.commit()
                flash('Load created!', 'alert-success')
            except Exception as ex:
                flash('Something went wrong, please try again later. If this continues please email meet.gio@icloud.com.', 'alert-danger')
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
            return try_commit_rollback(success='Location created!', fail='Something went wrong, please try again later. If this continues please email meet.gio@icloud.com.', route='/locations', duplicate="Location has already been added by another user. Locations have to be unqiue to each user. See our FAQ's for more info.")
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
            return try_commit_rollback(success='Carrier created!', fail='Something went wrong, please try again later. If this continues please email meet.gio@icloud.com.', route='/carriers')
    return render_template('user/carriers.html', form=form, carriers=carriers)

@app.route('/update_load/<int:load_id>', methods=['GET', 'POST'])
def update_load(load_id):
    '''Renders and handles the load data updates.'''
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/') 
    data = LoadData.query.filter_by(load_id=load_id).first()
    form = LoadDataForm(obj=data)
    if form.validate_on_submit():
        data.ontime = form.ontime.data
        data.damges = form.damages.data
        data.breakdown = form.breakdown.data
        data.cost = form.cost.data
        data.pallets = form.pallets.data
        data.weight = form.weight.data
        # Once object has been updated we commit.
        return try_commit(success='Load Data added!', fail='Something went wrong, please try again later. If this continues please email meet.gio@icloud.com.')
    return render_template('user/load.html', form=form)

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
        return try_commit(success='Location updated!', fail='Something went wrong, please try again later. If this continues please email meet.gio@icloud.com.')
    return render_template('user/update.html', form=form)

@app.route('/delivered/<int:load_id>', methods=['POST'])
def completed(load_id):
    '''Handles when a load is marked as delivered.'''
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')
    load = Load.query.filter_by(id=load_id).first()
    load_data = LoadData.query.filter_by(load_id=load_id).first()
    # Changes the delivered status.
    load.delivered = 1
    load_data.delivered = 1
    # Commits the change.
    return try_commit(success='Load was delivered!', fail='Something went wrong, please try again later. If this continues please email meet.gio@icloud.com.')

@app.route('/kpi')
def show_kpi():
    '''Gathers KPI's and renders results.'''
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')
    ontime = ontime_KPI()
    breakdown = breakdown_KPI()
    damages = damages_KPI()
    avg_load_cost = avg_cost_load()
    pallet_cost = cost_per_pallet()
    weight_cost = cost_per_lbs()
    return render_template('user/kpi.html', ontime=ontime, breakdown=breakdown, damages=damages, avg_load=avg_load_cost, avg_pallet=pallet_cost, avg_weight=weight_cost)

# 
# 404 PAGE
# 
@app.errorhandler(404)
def page_not_found(e):
    '''Custom 404 page'''
    return render_template('404.html'), 404
# 
# FAQ'S
# 
@app.route('/faqs')
def faq():
    return render_template('user/faqs.html')
