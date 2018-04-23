from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, url_for, redirect
from app.models import User
from app import app


@app.route('/')
@app.route('/index')
@login_required
def index(): 
    user = {'username': 'Jason'}
    # The render_template() function invokes the Jinja2 template engine that comes bundled with the Flask framework.
    return render_template('index.html', title='Home', user=user)

# This function will need to be changed to work with React as I am not using Flask to render my templates
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username='[insert username from form]').first()
    
    # Perform some server side validation of user details then log them in
    if user is None or not user.check_password('[insert password from form]'):
        print ('Invalid username or password')
        return redirect(url_for('login')) # Replace with response with bad username
    else:
        login_user(user, remember='[insert remember me status from form]')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    login_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Perform some server side validation of user details then add then
    user = User(username='[insert username from form]')
    user.set_password('[insert username from form]')
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login')) # Replace with successful api response