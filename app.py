from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy import text
from forms import RegisterUserForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///movies_example'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chickens'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('New User Added')
        return redirect('/secret')
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)
        if user:
            session['username'] = user.username
            return redirect('/secret')
    
    return render_template('login.html', form=form)

@app.route('/secret')
def secret():
    return render_template('secret.html')