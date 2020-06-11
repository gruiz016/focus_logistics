from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

# 
# USER MODEL
#   

class User(db.Model):
    '''Creates a users table in SQLAlchemy & PostgreSQL.'''
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    @classmethod
    def singup(cls, username, password):
        '''Sign's up a new user
        
        Uses Bcrypt to hash a password for security!
        '''
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        user = cls(username=username, password=hashed_pwd)
        
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
    
        return user

    @classmethod
    def authenticate(cls, username, password):
        '''Authenticates users.'''
        user = cls.query.filter_by(username=username).first()
        
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
            
        return False
    
    def __repr__(self):
        return f'<User id: {self.id}, username: {self.username}>'
# 
# DC MODEL
# 

class DistributionCenter(db.Model):
    '''Creates a DC (load destination) table in SQLAlchemy & PostgreSQL.'''    
    
    __tablename__ = 'distribution_centers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    name = db.Column(db.Text, unique=True, nullable=False)
    address = db.Column(db.Text, unique=True, nullable=False)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    zip = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @classmethod
    def get_dist_by_user(cls, user_id):
        '''Gets a list of distrubution centers that is linked to a user.'''
        
        dist_centers = cls.query.filter_by(user_id=user_id).all()
        return dist_centers
    
    def __repr__(self):
        return f'<DC id:{self.id}, name: {self.name}>'
# 
# CARRIER MODEL
# 

class Carrier(db.Model):
    '''Creates a carrier table in SQLAlchemy & PostgreSQL.'''
    
    __tablename__ = 'carriers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    zip = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @classmethod
    def get_carrier_by_user(cls, user_id):
        '''Gets a list of carriers that is linked to a user.'''
        
        carriers = cls.query.filter_by(user_id=user_id).all()
        return carriers
    
    def __repr__(self):
        return f'<Carrier. id:{self.id}, name: {self.name}>'
    
# 
# LOAD MODEL
# 

class Load(db.Model):
    '''Creates a load table in SQLAlchemy & PostgreSQL.'''
    
    __tablename__ = 'loads'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    po = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)   
    pickup_city = db.Column(db.Text, nullable=False)   
    pickup_state = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Text, nullable=True)
    day_of_week = db.Column(db.Text, nullable=True)
    temp = db.Column(db.Integer, nullable=False)
    team = db.Column(db.Integer, nullable=False)
    miles = db.Column(db.Integer, nullable=False, default=0)
    delivered = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carriers.id'), nullable=False)
    d_c_id = db.Column(db.Integer, db.ForeignKey('distribution_centers.id'), nullable=False)
    
    @classmethod
    def get_load_by_carrier(cls, carrier_id):
        '''Gets a list of loads that is linked to a carrier.'''
        
        loads = cls.query.filter_by(carrier_id=carrier_id).all()
        return loads
    
    @classmethod
    def get_load_by_dist_center(cls, d_c_id):
        '''Gets a list of loads that is linked to a distribution centers.'''
        
        loads = cls.query.filter_by(d_c_id=d_c_id).all()
        return loads
    
    def __repr__(self):
        return f'<Load. id:{self.id}, name: {self.name}>'
# 
# LOAD DATA MODEL
# 
class LoadData(db.Model):
    '''Creates a Data table for the loads in SQLAlchemy & PostgreSQL.'''

    __tablename__ = 'load_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    load_id = db.Column(db.Integer, db.ForeignKey('loads.id'), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 
    # Meaning of Inegers for load data
    # 
    # 0 = NO | 1 = YES
    # 
    ontime = db.Column(db.Integer, default=0)
    damges = db.Column(db.Integer, default=0)
    breakdown = db.Column(db.Integer, default=0)

    # Normal Int values
    cost = db.Column(db.Integer, default=0)
    pallets = db.Column(db.Integer, default=0)
    weight = db.Column(db.Integer, default=0)
    delivered = db.Column(db.Integer, default=0)
    
    @classmethod
    def get_load_data_by_load(cls, load_id):
        '''Gets a list of loads that is linked to a load.'''
        
        load = cls.query.filter_by(load_id=load_id).first()
        return load
    
    @classmethod
    def get_load_data_by_user(cls, user_id):
        '''Gets a list of loads that is linked to a user.'''
        
        loads = cls.query.filter_by(user_id=user_id).all()
        return loads
    
    def __repr__(self):
        return f'<Load Data id:{self.id}, load_id: {self.load_id}, user_id:{self.user_id}>'

    
    