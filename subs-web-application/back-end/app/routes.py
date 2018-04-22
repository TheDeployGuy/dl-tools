from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index(): 
    user = {'username': 'Jason'}
    # The render_template() function invokes the Jinja2 template engine that comes bundled with the Flask framework.
    return render_template('index.html', title='Home', user=user)