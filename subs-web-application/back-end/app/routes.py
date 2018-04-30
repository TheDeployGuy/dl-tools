from datetime import datetime, timedelta
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect, jsonify, request, make_response
from app.models import User, Entry
from app import app, db
import jwt
from functools import wraps

# This can now be used on all routes where login is required...
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        # Need a try catch block in case the token is not valid and it can't be decoded
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
            # todo: Think about better place for this...
            current_user.last_seen = datetime.utcnow()
            db.session.commit()
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Since this is the 2nd function called, we know we can already get the token...
        token = request.headers['x-access-token']
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
            if current_user.is_admin == False:
                return jsonify({'message': 'Permission Denied'}), 401
        except:
            return jsonify({'message': 'admin invalid'}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index(): 
    # todo: Render react index.html (maybe)
    # The render_template() function invokes the Jinja2 template engine that comes bundled with the Flask framework.
    return render_template('index.html')

# This function will need to be changed to work with React as I am not using Flask to render my templates
@app.route('/api/login', methods=['POST', 'GET'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify login details', 401, {
            'WWW-Authenticate': 'Basic realm="Login Required"'
        })

    user = User.query.filter_by(username=auth['username']).first()
    
    # Perform some server side validation of user details then log them in
    if user is None or not user.check_password(auth['password']):
        return jsonify({ 'message': 'Invalid username or password'})
    else:
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        #todo: Return more details
        return jsonify({ 'token' : token.decode('UTF-8')})

@app.route('/api/logout')
def logout():
    # logout_user()
    return redirect(url_for('index'))

########### User Account Routes ####################
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
@token_required
@admin_required
def get_all_users(current_user):
    return jsonify([e.to_dict() for e in User.query.all()])

@app.route('/api/user/<username>', methods=['GET'])
@token_required
def get_one_user(current_user, username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.to_dict())


@app.route('/api/user/<username>', methods=['PUT'])
@token_required
def update_user(current_user, username):
    form_data = request.get_json()
    user = User.query.filter_by(username=username).first_or_404()

    # Add checks for if the username has changed etc...
    user.username = form_data['username']
    user.set_password(form_data['password'])

    db.session.commit()

    return jsonify({'message': 'The user has been updated...'})


@app.route('/api/user/<username>/promote', methods=['PUT'])
@token_required
@admin_required
def promote_user(current_user, username):
    form_data = request.get_json()
    user = User.query.filter_by(username=username).first_or_404()
    user.promote_user()
    db.session.commit()

    return jsonify({'message': 'The user has been promoted to an admin...'})

@app.route('/api/user/<username>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User has been deleted'})


############# Entries Routes ###################
@app.route('/api/entry', methods=['POST'])
@token_required
def add_entry(current_user):
    form_data = request.get_json()

    entry = Entry(details=form_data['details'], user_id=current_user['id'])
    db.session.add(entry)
    db.session.commit()

    return jsonify({'message': 'New Subs Entry has been created...'})

@app.route('/api/entry', methods=['GET'])
@token_required
def get_entries(current_user):
    return jsonify([e.to_dict for e in Entry.query.all()])

@app.route('/api/entry/<id>', methods=['GET'])
@token_required
def get_entry(current_user, id):
    # Get specific entry, need to add check to get Entries for a specific user
    entry = Entry.query.filter_by(id=id).first_or_404()
    return jsonify({'entry': entry})

# Update entry
@app.route('/api/entry/<id>', methods=['PUT'])
@token_required
def update_entry(current_user, id):
    form_data = request.get_json()
    entry = Entry.query.filter_by(id=id).first_or_404()

    # update entry here...
    entry.details = form_data['details']

    db.session.commit()

    return jsonify({ 'message': 'Entry Updated Successfully...' })
    
# Delete entry
@app.route('/api/entry/<id>', methods=['DELETE'])
@token_required
def delete_entry(current_user, id):
    entry = Entry.query.filter_by(id=id).first_or_404()
    db.session.delete(entry)
    db.session.commit()

    return jsonify({'message': 'Subs Entry has been deleted'})