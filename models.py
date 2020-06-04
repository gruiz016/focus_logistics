from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
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
        
        db.session.add(user)
        db.session.commit()
        
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
        
class DistributionCenter(db.Model):
    '''Creates a DC (load destination) table in SQLAlchemy & PostgreSQL.'''    
    
    __tablename__ = 'distribution_centers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    name = db.Column(db.Text, unique=True, nullable=False)
    address = db.Column(db.Text, unique=True, nullable=False)
    city = db.Column(db.Text, nullable=False)
    zip = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @classmethod
    def get_dist_by_user(cls, user_id):
        '''Gets a list of distrubution centers that is linked to user.'''
        
        dist_centers = cls.query.filter_by(user_id=user_id).all()
        return dist_centers
    
    def __repr__(self):
        return f'<DC id:{self.id}, name: {self.name}>'
    
class Carrier(db.Model):
    '''Creates a carrier table in SQLAlchemy & PostgreSQL.'''
    
    __tablename__ = 'carriers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.Text, unique=True, nullable=False)
    address = db.Column(db.Text, unique=True, nullable=False)
    city = db.Column(db.Text, nullable=False)
    zip = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @classmethod
    def get_carrier_by_user(cls, user_id):
        '''Gets a list of distrubution centers that is linked to user.'''
        
        carriers = cls.query.filter_by(user_id=user_id).all()
        return carriers
    
    def __repr__(self):
        return f'<Carrier. id:{self.id}, name: {self.name}>'
    