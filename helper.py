'''Below are functions that help with app functionality.'''
from flask import flash, redirect, session

def check_if_logged_in():
    if 'user_id' not in session:
        flash('You must be logged to access', 'alert-danger')
        return redirect('/')