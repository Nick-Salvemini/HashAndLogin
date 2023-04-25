from flask import Flask, session, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from sqlalchemy import text
from forms import RegisterUserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hash_and_login_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chickens'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    if 'username' in session: 
        user = User.query.get_or_404(session['username'])
        return redirect(f'/users/{user.username}')
    else:
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
        return redirect(f'/users/{new_user.username}')
    
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
            return redirect(f'/users/{user.username}')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/<username>')
def user_info(username):
    user = User.query.get_or_404(username)
    feedbacks = Feedback.query.filter_by(username=user.username)
    if 'username' not in session or session['username'] != user.username:
        flash('User must be logged in to view user data')
        return redirect('/login')
    else:
        return render_template('user.html', user=user, feedbacks=feedbacks)
    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    user = User.query.get_or_404(username)
    feedbacks = Feedback.query.filter_by(username=user.username).all()
    if 'username' in session and session['username'] == user.username:
        db.session.delete(user)
        for feedback in feedbacks:
            db.session.delete(feedback)
        db.session.commit()
        session.clear()
        return redirect('/')
    else:
        flash('User must be logged in to delete')
        return redirect('/login')
    
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    user = User.query.get_or_404(username)
    form = FeedbackForm()
    if 'username' in session and session['username'] == user.username:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template('feedback.html', form=form, user=user)
    else:
        return redirect('/')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    user = User.query.get_or_404(feedback.username)
    form = FeedbackForm(obj=feedback)
    if 'username' in session and session['username'] == user.username:
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{user.username}')
        else:
            return render_template('edit_feedback.html', form=form, user=user, feedback=feedback)
    else:
        return redirect('/')

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    user = User.query.get_or_404(feedback.username)
    if 'username' in session and session['username'] == user.username:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{user.username}')
    else:
        return redirect('/')