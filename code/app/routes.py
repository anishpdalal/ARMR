from app import application, db
from flask import render_template, redirect, url_for, \
    flash, request, session, g
from flask_login import current_user, login_user, login_required, logout_user
from app.classes import User
from app.forms import LogInForm, RegistrationForm, UploadFileForm
from app import db, login_manager
from datetime import timedelta
from flask_wtf import FlaskForm
from werkzeug import secure_filename
import os


@application.route('/', methods=('GET', 'POST'))
@application.route("/index")
def index():
    login_form = LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = User.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('upload'))
        else:
            flash('Invalid username and password combination!')

    return render_template('index.html', form=login_form)


@application.before_request
def make_session_permanent():
    session.permanent = True
    application.permanent_session_lifetime = timedelta(minutes=30)


@login_manager.user_loader
def load_user(id):  # id is the ID in User.
    return User.query.get(int(id))


@application.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form, null=True, blank=True)
    if request.method == 'POST':
        if form.validate() is False:
            flash(form.errors)  # spits out any and all errors

    if form.validate_on_submit():
        user = User(form.username.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """upload a file from a client machine."""
    file = UploadFileForm()  
    if file.validate_on_submit():  
        f = file.file_selector.data  
        filename = secure_filename(f.filename)
        file_dir_path = os.path.join(application.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)
        f.save(file_path) # Save file to file_path (instance/ + 'files' + filename)

        return redirect(url_for('results'))  # Redirect to / (/index) page.
    return render_template('upload.html', form=file)


@application.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    """upload a file from a client machine."""
    return render_template('results.html')
