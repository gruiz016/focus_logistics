'''Below are functions that help with app functionality.'''
from flask import flash, redirect, session
from models import Carrier, DistributionCenter

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