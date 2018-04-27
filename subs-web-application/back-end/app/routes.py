from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, url_for, redirect, jsonify, request
from app.models import User, Entry
from app import app


# This is executed right before the view function, update last_seen of the user
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/register', methods=['GET', 'POST'])
def register():
    form_data = request.get_json()

    # Perform some server side validation of user details then add then
    user = User(username=form_data['username'])
    user.set_password(form_data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'New User created...'})

@app.route('/api/user', methods=['GET'])
def get_all_users():
    return jsonify([e.to_dict for e in User.query.all()])

@app.route('/api/user/<username>', methods=['GET'])
@login_required
def get_one_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.to_dict())


@app.route('/api/user/<username>', methods=['PUT'])
def update_user(username):
    form_data = request.get_json()
    user = User.query.filter_by(username=username).first_or_404()

    user.username = form_data['username']
    user.set_password(form_data['password'])

    db.session.commit()

    return jsonify({'message': 'The user has been updated...'})


@app.route('/api/user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User has been deleted'})

@app.route('/api/entries', methods=['GET'])
def get_entries():
    return jsonify([e.to_dict for e in Entry.query.all()])

@app.route('/api/entries/<id>', methods=['GET'])
def get_entry(id):
    # Get specific entry, need to add check to get Entries for a specific user
    entry = Entry.query.filter_by(id=id).first_or_404()
    return jsonify({'entry': entry})


