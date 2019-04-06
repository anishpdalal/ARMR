from app import application, classes, db
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/register')
def register():
    username = 'diane'
    password = 'pwd'
    email='diane@gmail.com'

    user_count = classes.User.query.filter_by(username=username).count() \
                    + classes.User.query.filter_by(email=email).count()

    if user_count > 0:
        return '<h1> Error - Existing user : ' + username + ' or ' + email + '</h1>'

    else:
        user = classes.User(username, email, password)
        db.session.add(user)
        db.session.commit()
        return '<h1> Registered : ' + username + '</h1>'


@application.route('/login', methods=['GET', 'POST'])
def login():
    username = 'diane'
    password = 'pwd'
    # Look for it in the database.
    user = classes.User.query.filter_by(username=username).first()

    # Login and validate the user.
    if user is not None and user.check_password(password):
        login_user(user)
        return redirect(url_for('secret_page'))

    else:
        return '<h1> Invalid username and password combination! </h1>'


@application.route('/logout')
@login_required
def logout():
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    return before_logout + after_logout


@application.route('/secret_page')
@login_required
def secret_page():
    return render_template('secret.html', name=current_user.username, email=current_user.email)


