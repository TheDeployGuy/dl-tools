from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
# DB instance with the flask instance passed to it
db = SQLAlchemy(app)
# Migrate instance takes the flask instance and the db instance
migrate = Migrate(app, db)



# The bottom import is a workaround to circular imports, a common problem with Flask applications
from app import routes, models