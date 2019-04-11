from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, \
    SelectField, FileField, IntegerField
from wtforms.validators import DataRequired, InputRequired, ValidationError
from flask_wtf.file import FileRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username (Email):', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password_confirmation = PasswordField('Repeat Password:',
                                          validators=[DataRequired()])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class UploadFileForm(FlaskForm):
    """Class for uploading file when submitted"""
    mrn = IntegerField('Medical Record Number (MRN)', validators=[InputRequired()])
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')

    def validate_mrn(form, field):
        if len(str(field.data)) != 7:
            raise ValidationError('MRN must be 7 digits.')

class ModelResultsForm(FlaskForm):
    """Class for uploading file when submitted"""
    submit = SubmitField('Submit')
