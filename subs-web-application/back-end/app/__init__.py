from flask import Flask

app = Flask(__name__)

# The bottom import is a workaround to circular imports, a common problem with Flask applications
from app import routes