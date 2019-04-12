from app import application, db
from flask import render_template, redirect, url_for, \
    flash, request, session, g
from flask_login import current_user, login_user, login_required, logout_user
from app.classes import User, Data
from app.forms import LogInForm, RegistrationForm, UploadFileForm, \
    ModelResultsForm
from app.nlp import prepare_note
from app import db, login_manager, spacy_model
from datetime import timedelta, datetime
from flask_wtf import FlaskForm
from werkzeug import secure_filename
from app.static_result import example_result
import speech_recognition as sr
import os
import uuid
import re
import pytz


@application.route('/', methods=('GET', 'POST'))
@application.route("/index", methods=('GET', 'POST'))
def index():
    """The homepage for the website."""
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


@login_manager.user_loader
def load_user(id):  # id is the ID in User.
    """Finds the user with the given user id."""
    return User.query.get(id)


@application.route('/register', methods=('GET', 'POST'))
def register():
    """Page for new users to register."""
    form = RegistrationForm(request.form, null=True, blank=True)

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
    """Log out the user."""
    logout_user()
    return redirect(url_for('index'))


@application.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Upload a file from a client machine."""
    file = UploadFileForm()
    if file.validate_on_submit():
        f = file.file_selector.data
        filename = secure_filename(f.filename)
        file_dir_path = os.path.join(application.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)
        # Save file to file_path (instance/ + 'files' + filename)
        f.save(file_path)

        file_dir_path = os.path.join(application.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)

        # Convert audio file to text (String)
        r = sr.Recognizer()
        harvard = sr.AudioFile(file_path)
        with harvard as source:
            audio = r.record(source)
        talk_to_text = r.recognize_google(audio)

        # pipe results from talk to text to nlp model
        example_result = prepare_note(spacy_model, talk_to_text)

        """Display the model results."""
        proper_title_keys = [k.title() for k in list(example_result.keys())]

        session['example_result'] = example_result
        session['proper_title_keys'] = proper_title_keys

        # delete the file
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("The file does not exist.")

        return redirect(url_for('results', filename=filename))
    return render_template('upload.html', form=file)


@application.route('/results/<filename>', methods=['GET', 'POST'])
@login_required
def results(filename):
    example_result = session.get('example_result', None)
    proper_title_keys = session.get('proper_title_keys', None)

    form = ModelResultsForm()
    if form.validate_on_submit():

        physician_id = 2
        transcription_id = 1
        row_info = list()
        tz = pytz.timezone("US/Pacific")
        timestamp = datetime.now(tz)
        for sub in proper_title_keys:
            txt = example_result[sub.lower()]["text"]
            for ent_d in example_result[sub.lower()]["diseases"]:
                row_info.append((sub, txt, "disease", ent_d["name"]))
            for ent_m in example_result[sub.lower()]["medications"]:
                row_info.append((sub, txt, "medication", ent_m["name"]))
        for t in range(len(row_info)):
            sub_id = row_info[t][0]
            txt = row_info[t][1]
            entity = row_info[t][3]
            label = row_info[t][2]
            start = re.search(entity, txt).start()
            end = re.search(entity, txt).end() - 1
            upload_row = Data(physician_id=physician_id,
                              transcription_id=transcription_id,
                              text=txt,
                              entity=entity,
                              start=start,
                              end=end,
                              label=label,
                              subject_id=sub_id,
                              timestamp=timestamp)
            db.session.add(upload_row)
        db.session.commit()

        # TODO: query physician id
        # TODO: autogenerate transcription id (or maybe make this
        # an identifying string?)

        return redirect(url_for('upload'))

    return render_template('results.html', form=form, titles=proper_title_keys,
                           result=example_result)
