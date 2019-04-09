from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(120), nullable=False)

    def __init__(self, code):
        self.code = code

    def check_code(self, input):
        return check_password_hash(self.code, input)

    def check_pwd_digit(self, input):
        return any([x.isdigit() for x in input])

    def check_pwd_upper(self, input):
        return any([x.isupper() for x in input])

    def check_pwd_length(self, input):
        return len(input) >= 8


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


db.create_all()
db.session.commit()
