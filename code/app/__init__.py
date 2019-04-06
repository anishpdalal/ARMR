from flask import Flask
from flask_bootstrap import Bootstrap
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialization
# Create an application instance (an object of class Flask)  which handles all requests.
application = Flask(__name__)
application.secret_key = os.urandom(24)
application.config.from_object(Config)
db = SQLAlchemy(application)
db.create_all()
db.session.commit()

Bootstrap(application)

# login_manager needs to be initiated before running the app
login_manager = LoginManager()
login_manager.init_app(application)

from app import classes
from app import routes  # Added at the bottom to avoid circular dependencies. (Altough it violates PEP8 standards)
