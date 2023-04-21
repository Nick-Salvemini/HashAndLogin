from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
