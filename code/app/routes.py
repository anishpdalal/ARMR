from app import application, db
from flask import render_template, redirect, url_for, \
    flash, request, session, g
from flask_login import current_user, login_user, login_required, logout_user
from app.classes import User, Data
from app.forms import LogInForm, RegistrationForm, UploadFileForm
from app import db, login_manager
from datetime import timedelta
from flask_wtf import FlaskForm
from werkzeug import secure_filename
from app.static_result import example_result
import os
import uuid


@application.route('/', methods=('GET', 'POST'))
@application.route("/index", methods=('GET', 'POST'))
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
    return User.query.get(id)


@application.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form, null=True, blank=True)
    if request.method == 'POST':
        if form.validate() is False:
            flash(form.errors)  # spits out any and all errors

    if form.validate_on_submit():
        ph_id = str(uuid.uuid4())
        user = User(ph_id=ph_id,
                    username=form.username.data,
                    password=form.password.data)
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
        f.save(file_path)  # Save file to file_path (instance/ + 'files' + filename)

        return redirect(url_for('results'))  # Redirect to / (/index) page.
    return render_template('upload.html', form=file)


@application.route('/results/', methods=['GET', 'POST'])
@login_required
def results():
    """Display the model results."""
    proper_title_keys = [k.title() for k in list(example_result.keys())]

    """upload a file from a client machine."""

    ind = 0
    physician_id = 4
    transcription_id = 4
    text = "Give patient bandaid."
    entity = "band-aid"
    start = 13
    end = 19
    label = "medication"
    subject_id = 2

    upload = Data(index=ind,
                  physician_id=physician_id,
                  transcription_id=transcription_id,
                  text=text,
                  entity=entity,
                  start=start,
                  end=end,
                  label=label,
                  subject_id=subject_id)

    db.session.add(upload)
    db.session.commit()
    return render_template('results.html', titles=proper_title_keys, result=example_result)
