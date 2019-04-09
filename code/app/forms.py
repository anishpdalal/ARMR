from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


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
