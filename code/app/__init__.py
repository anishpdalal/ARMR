from flask import Flask
from flask_bootstrap import Bootstrap
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import FlaskForm
import spacy
from spacy.matcher import Matcher, PhraseMatcher


# Initialization
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

# load the spacy model
par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
spacy_model = spacy.load("{}/models/en_ner_bc5cdr_md-0.1.0".format(par_dir))

from app import classes
from app import routes  # Added at the bottom to avoid circular dependencies
