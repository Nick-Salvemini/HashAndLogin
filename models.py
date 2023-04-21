from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    '''A Model to store basic user data'''

    username = db.Column(db.String(20), 
                         primary_key=True)
    password = db.Column(db.Text,
                        nullable=False)
    email = db.Column(db.String(50),
                      unique=True,
                        nullable=False)
    first_name = db.Column(db.String(30),
                        nullable=False)
    last_name = db.Column(db.String(30),
                        nullable=False)
    
    def __repr__(self):
        u = self
        return f'<User - Username: {self.username} ; Password: {self.password} ; Email: {self.email} ; First Name: {self.first_name} ; Last Name: {self.last_name}>'
    
    @classmethod
    def register(cls, username, password):
        '''register a user with their username and hash their password'''

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
        
        return cls(username=username, password=hashed_utf8)


    @classmethod
    def login(cls, username, password):
        '''log in a user based on their username and password'''

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False