'''Below are functions that help with app functionality.'''
from flask import flash, redirect, session
from models import Carrier, DistributionCenter, LoadData
import requests

BASE_URL = 'http://www.mapquestapi.com/directions/v2/route'

def get_user_carriers():
    carriers = Carrier.get_carrier_by_user(user_id=session['user_id'])
    tup_carriers = []
    for carrier in carriers:
        tup_carriers.append((carrier.id, carrier.name))
        
    return tup_carriers

def get_dc():
    dc = DistributionCenter.get_dist_by_user(user_id=session['user_id'])
    tup_dc = []
    for d in dc:
        tup_dc.append((d.id, d.name))
        
    return tup_dc

def get_miles(app, dc_id, city, state):
    dc = DistributionCenter.query.filter_by(id=dc_id).first()
    response = requests.get(url=BASE_URL, params={'key': app, 'from': f'{city}, {state}', 'to': f'{dc.city}, {dc.state}'})
    data = response.json()
    return data['route']['distance']

def ontime_KPI():
    load_data = LoadData.query.filter_by(delivered=1).all()
    sum = 0
    count = 0
    for load in load_data:
        if load.ontime == 1:
            sum = sum + 1
            count += 1
        else:
            count += 1
    avg = (sum / count) * 100
    return round(avg , 2)

def damages_KPI():
    load_data = LoadData.query.filter_by(delivered=1).all()
    sum = 0
    count = 0
    for load in load_data:
        if load.damges == 1:
            sum = sum + 1
            count += 1
        else:
            count += 1
    avg = (sum / count) * 100
    return round(avg , 2)

def breakdown_KPI():
    load_data = LoadData.query.filter_by(delivered=1).all()
    sum = 0
    count = 0
    for load in load_data:
        if load.breakdown == 1:
            sum = sum + 1
            count += 1
        else:
            count += 1
    avg = (sum / count) * 100
    return round(avg , 2)

def avg_cost_load():
    load_data = LoadData.query.filter_by(delivered=1).all()
    sum = 0
    count = 0
    for load in load_data:
        sum += load.cost
        count += 1
    avg = sum / count
    return round(avg , 2)

def cost_per_pallet():
    load_data = LoadData.query.filter_by(delivered=1).all()
    sum_cost = 0
    sum_pallets = 0
    for load in load_data:
        sum_cost += load.cost
        sum_pallets += load.pallets
    avg = sum_cost / sum_pallets
    return round(avg , 2)

def cost_per_lbs():
    load_data = LoadData.query.filter_by(delivered=1).all()
    sum_cost = 0
    sum_weight = 0
    for load in load_data:
        sum_cost += load.cost
        sum_weight += load.weight
    avg = sum_cost / sum_weight
    return round(avg , 2)

    