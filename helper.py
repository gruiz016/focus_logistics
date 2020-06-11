'''Below are functions that help with app functionality.'''
from flask import flash, redirect, session
from models import Carrier, DistributionCenter, LoadData, db
import requests

BASE_URL = 'http://www.mapquestapi.com/directions/v2/route'

def get_user_carriers():
    '''Creates a tuple per user to create a selectfield with WTForms'''
    carriers = Carrier.get_carrier_by_user(user_id=session['user_id'])
    tup_carriers = []
    for carrier in carriers:
        tup_carriers.append((carrier.id, carrier.name))    
    return tup_carriers

def get_dc():
    '''Creates a tuple per user to create a selectfield with WTForms'''
    dc = DistributionCenter.get_dist_by_user(user_id=session['user_id'])
    tup_dc = []
    for d in dc:
        tup_dc.append((d.id, d.name))
    return tup_dc

def get_miles(app, dc_id, city, state):
    '''Calls MapQuest API to get current location.'''
    dc = DistributionCenter.query.filter_by(id=dc_id).first()
    response = requests.get(url=BASE_URL, params={'key': app, 'from': f'{city}, {state}', 'to': f'{dc.city}, {dc.state}'})
    data = response.json()
    return data['route']['distance']

def ontime_KPI():
    '''Returns the AVG of ontime loads.'''
    load_data = LoadData.query.filter(LoadData.delivered==1, LoadData.user_id == session['user_id']).all()
    sum = 0
    count = 0
    for load in load_data:
        if load.ontime == 1:
            sum = sum + 1
            count += 1
        else:
            count += 1
    try:
        avg = (sum / count) * 100
    except ZeroDivisionError:
        avg = 0
    return round(avg , 2)

def damages_KPI():
    '''Returns the AVG of damaged loads.'''
    load_data = LoadData.query.filter(LoadData.delivered==1, LoadData.user_id == session['user_id']).all()
    sum = 0
    count = 0
    for load in load_data:
        if load.damges == 1:
            sum = sum + 1
            count += 1
        else:
            count += 1
    try:
        avg = (sum / count) * 100
    except ZeroDivisionError:
        avg = 0
    return round(avg , 2)

def breakdown_KPI():
    '''Returns the AVG of brokendown loads.'''
    load_data = LoadData.query.filter(LoadData.delivered==1, LoadData.user_id == session['user_id']).all()
    sum = 0
    count = 0
    for load in load_data:
        if load.breakdown == 1:
            sum = sum + 1
            count += 1
        else:
            count += 1
    try:
        avg = (sum / count) * 100
    except ZeroDivisionError:
        avg = 0
    return round(avg , 2)

def avg_cost_load():
    '''Returns the AVG cost of loads.'''
    load_data = LoadData.query.filter(LoadData.delivered==1, LoadData.user_id == session['user_id']).all()
    sum = 0
    count = 0
    for load in load_data:
        sum += load.cost
        count += 1
    try:
        avg = sum / count
    except ZeroDivisionError:
        avg = 0
    return round(avg , 2)

def cost_per_pallet():
    '''Returns the AVG cost per pallet.'''
    load_data = LoadData.query.filter(LoadData.delivered==1, LoadData.user_id == session['user_id']).all()
    sum_cost = 0
    sum_pallets = 0
    for load in load_data:
        sum_cost += load.cost
        sum_pallets += load.pallets
    try:
        avg = sum_cost / sum_pallets
    except ZeroDivisionError:
        avg = 0
    return round(avg , 2)

def cost_per_lbs():
    '''Returns the AVG cost oer pound.'''
    load_data = LoadData.query.filter(LoadData.delivered==1, LoadData.user_id == session['user_id']).all()
    sum_cost = 0
    sum_weight = 0
    for load in load_data:
        sum_cost += load.cost
        sum_weight += load.weight
    try:
        avg = sum_cost / sum_weight
    except ZeroDivisionError:
        avg = 0
    return round(avg , 2)

def try_commit(success, fail):
    '''Tries to commit changes to DB. If something goes wrong, will redirect.'''
    try:
        db.session.commit()
        flash(f'{success}', 'alert-success')
    except Exception as ex:
        flash(f'{fail}', 'alert-danger')
    return redirect('/manage')

def try_commit_rollback(success, fail, route, duplicate='This has already been added. Please try again.'):
    '''Tries to commit changes to DB. If something goes wrong, will redirect and rollback.'''
    try:
        db.session.commit()
        flash(f'{success}', 'alert-success')
    except Exception as ex:
        msg = str(ex)
        db.session.rollback()
        if 'duplicate key value violates unique constraint' in msg:
            flash(f"{duplicate}", 'alert-danger')
        else:
            flash(f'{fail}', 'alert-danger')
    return redirect(f'{route}')

def try_signup(id, success, fail, route, duplicate='This has already been added. Please try again.'):
    '''Tries to commit changes to DB. If something goes wrong, will redirect, rollback and pop user session.'''
    try:
        session['user_id'] = id
        db.session.commit()
        flash(f'{success}', 'alert-success')
    except Exception as ex:
        msg = str(ex)
        db.session.rollback()
        session.pop('user_id')
        if 'duplicate key value violates unique constraint' in msg:
            flash(f"{duplicate}", 'alert-danger')
        else:
            flash(f'{fail}', 'alert-danger')
    return redirect(f'{route}')


    