'''Below are functions that help with app functionality.'''
from flask import flash, redirect, session
from models import Carrier, DistributionCenter
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