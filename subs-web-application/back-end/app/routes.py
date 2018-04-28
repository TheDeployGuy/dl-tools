from datetime import datetime, timedelta
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect, jsonify, request, make_response
from app.models import User, Entry
from app import app, db
import jwt

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#     pass

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
@app.route('/login', methods=['POST', 'GET'])
def login():
    auth = request.authorization

    print(auth)
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

@app.route('/logout')
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
def get_all_users():
    return jsonify([e.to_dict() for e in User.query.all()])

@app.route('/api/user/<username>', methods=['GET'])
def get_one_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.to_dict())


@app.route('/api/user/<username>', methods=['PUT'])
def update_user(username):
    form_data = request.get_json()
    user = User.query.filter_by(username=username).first_or_404()

    # Add checks for if the username has changed etc...
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


############# Entries Routes ###################
@app.route('/api/entry', methods=['POST'])
def add_entry():
    form_data = request.get_json()

    entry = Entry(details=form_data['details'], user_id=form_data['user_id'])
    db.session.add(entry)
    db.session.commit()

    return jsonify({'message': 'New Subs Entry has been created...'})

@app.route('/api/entry', methods=['GET'])
def get_entries():
    return jsonify([e.to_dict for e in Entry.query.all()])

@app.route('/api/entry/<id>', methods=['GET'])
def get_entry(id):
    # Get specific entry, need to add check to get Entries for a specific user
    entry = Entry.query.filter_by(id=id).first_or_404()
    return jsonify({'entry': entry})

# Update entry
@app.route('/api/entry/<id>', methods=['PUT'])
def update_entry(id):
    form_data = request.get_json()
    entry = Entry.query.filter_by(id=id).first_or_404()

    # update entry here...
    entry.details = form_data['details']

    db.session.commit()

    return jsonify({ 'message': 'Entry Updated Successfully...' })
    

# Delete entry
@app.route('/api/entry/<id>', methods=['DELETE'])
def delete_entry(id):
    entry = Entry.query.filter_by(id=id).first_or_404()
    db.session.delete(entry)
    db.session.commit()

    return jsonify({'message': 'Subs Entry has been deleted'})