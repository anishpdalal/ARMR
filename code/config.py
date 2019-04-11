import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "week3.db")
    """Connect to database."""
    # user = "armrMaster"  # replace with server username
    # pw = "armr_pw603"  # replace with server password
    # user = "tylerursuy"
    # pw = "T062096u"
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{pw}@armr.c4eooxhj8ss8.us-west-1.rds.amazonaws.com:5432/armr"
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{pw}@localhost:5432/armr"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
