from app import application, classes, db
from flask import render_template, redirect, url_for, flash, request, session, g
from flask_login import current_user, login_user, login_required, logout_user
from classes import LogInForm, RegistrationForm, User
from app import db, login_manager
from datetime import timedelta
from flask_wtf import FlaskForm


@application.route('/')
def index():
    return render_template('index.html')


@application.before_request
def make_session_permanent():
    flash('asdf')
    session.permanent = True
    application.permanent_session_lifetime = timedelta(minutes=30)


@login_manager.user_loader
def load_user(id):  # id is the ID in User.
    return User.query.get(int(id))


@application.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form, null=True, blank=True)
    if request.method == 'POST':
        if form.validate() == False:
            flash(form.errors) #spits out any and all errors**

    if form.validate_on_submit():
        flash('fds')
        user = User(form.username.data,
                    form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LogInForm()
    if True:
        username = login_form.username.data
        password = login_form.password.data

        # Look for it in the database.
        user = User.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('secret_page'))
        else:
            flash('Invalid username and password combination!')

    return render_template('login.html', form=login_form)


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
    return render_template('secret.html', name=current_user.username)

