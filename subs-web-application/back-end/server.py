from app import app, db
from app.models import User, Entry

# Instead of using just the python interperator we can use the flask shell which will automatically import and configure the context for our application for easier debugging and playing around.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Entry': Entry}