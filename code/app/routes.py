from app import application, classes, db
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from classes import LogInForm, RegistrationForm

@application.route('/')
def index():
    return render_template('index.html')


@application.route('/register', methods=('GET', 'POST'))
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        # password_confirmation = registration_form.password_confirmation.data
        # verification_code_input = registration_form.access_code.data
        
        # verification = Verification.query.first() 

        # user_count = User.query.filter_by(username=username).count()

        # error_count = 0
        # if(password != password_confirmation):
        #     error_count = error_count + 1 
        #     flash('Error - Password Mismatch<br/>' )
        
        # if(not verification.check_code(verification_code_input)):
        #     error_count = error_count + 1 
        #     flash('Error - Invalid Access Code<br/>' )

        # if(not (verification.check_pwd_digit(password) and verification.check_pwd_upper(password) and verification.check_pwd_length(password))):
        #     error_count = error_count + 1 
        #     flash('Error - Password should be at least 8 digits with at least one number and one uppercase<br/>' )
        
        # if(user_count > 0):
        #     error_count = error_count + 1 
        #     flash('Error - Existing user : ' + username + '<br/>')
            
        # if(error_count == 0):
        #     user = User(username, password)
        #     db.session.add(user)
        #     db.session.commit()
        #     return redirect(url_for('login'))
            
	return render_template('register.html', form=registration_form)


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


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LogInForm()
#     if login_form.validate_on_submit():
#         username = login_form.username.data
#         password = login_form.password.data
#         # Look for it in the database.
#         user = User.query.filter_by(username=username).first()

#         # Login and validate the user.
#         if user is not None and user.check_password(password):
#             login_user(user)
#             return redirect(url_for('alert'))
#         else:
#             flash('Invalid username and password combination!')
# 	return render_template('login.html', form=login_form)


@application.route('/logout')
@login_required
def logout():
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    return before_logout + after_logout


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
# return redirect(url_for('index'))


@application.route('/secret_page')
@login_required
def secret_page():
    return render_template('secret.html', name=current_user.username, email=current_user.email)


