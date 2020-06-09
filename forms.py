from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Length

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

choice = [(0, "NO"), (1, "YES")]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Confirm Password')
    
class DCCarrierForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=[(st, st) for st in states])
    zip = StringField('Zip Code')
    phone = IntegerField('Phone Number')
    
class LoadForm(FlaskForm):
    po = StringField('PO Number', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=[(st, st) for st in states])
    due_date = DateField('Due Date', validators=[DataRequired()], format='%m/%d/%Y')
    day_of_week = SelectField('Day Of Week', choices=[(d, d) for d in days])
    temp = IntegerField('Temperture (F)', validators=[DataRequired()])
    team = SelectField('Team', choices=[c for c in choice], coerce=int)
    carrier_id = SelectField('Carrier', coerce=int)
    d_c_id = SelectField('Distribution Center', coerce=int)
    
class UpdateLocationForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=[(st, st) for st in states])
    
class LoadDataForm(FlaskForm):
    ontime = SelectField('Was load ontime?', choices=[c for c in choice], coerce=int)
    damages = SelectField('Any damages?', choices=[c for c in choice], coerce=int)
    breakdown = SelectField('Any breakdowns?', choices=[c for c in choice], coerce=int)
    cost = IntegerField('Price (USD $)', validators=[DataRequired()])
    pallets = IntegerField('Pallets', validators=[DataRequired()])
    weight = IntegerField('Weight (LBS)', validators=[DataRequired()])
    
