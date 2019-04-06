from flask import Flask
from flask_bootstrap import Bootstrap
import os

# Initialization
# Create an application instance (an object of class Flask)  which handles all requests.
application = Flask(__name__)
application.secret_key = os.urandom(24)
Bootstrap(application)

from app import routes  # Added at the bottom to avoid circular dependencies. (Altough it violates PEP8 standards)

