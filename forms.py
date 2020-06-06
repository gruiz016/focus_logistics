from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Confirm Password')
    
class DistributionCenterForm(FlaskForm):
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    
    name = StringField('Facility Name', validators=[DataRequired()])
    address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=[(st, st) for st in states])
    zip = IntegerField('Zip Code', validators=[Length(min=6, max=6, message='Please enter valid zip code.')])
    phone = IntegerField('Phone Number', validators=[Length(min=10, max=10, message='Please enter phone number with no dashes.')])