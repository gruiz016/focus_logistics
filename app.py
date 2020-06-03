from flask import Flask, request, render_template, redirect, flash, session, jsonify
from models import db, connect_db
import requests
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///freight_db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'This_is_a_secret!')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home():
    return render_template('home.html')