#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, current_app, session, redirect
from flask_sqlalchemy import SQLAlchemy
from backend_requests import get_data, process_data
from flask.json import jsonify
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from data.insert_resources import insertRes
import pyrebase
current_user = {}
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
config = app.config["API_KEY"]
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
# insert resources
# insertRes(db)


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/gym')
def bothGym():
    # if 'usr' not in session:
    #     print("\nNot logged in...")
    # else:
    #     print("\nUser is logged in...")
    #     print("Email:", session['email'])
    all_resources = []
    all_resources.append("Equipment Information")
    all_resources.append(get_data.get_all_resources(db))
    return render_template('pages/gym.html', data=all_resources)



@app.route('/brodie')
def brodie():
    return render_template('pages/brodie.html')

@app.route('/brodieEquipment')
def brodieGym():
    if 'usr' not in session:
        print("\nNot logged in...")
    else:
        print("\nUser is logged in...")
        print("Email:", session['email'])
    brodie_resources = []
    brodie_resources.append("Brodie Equipment")
    brodie_resources.append(get_data.get_filtered_data(
        db, "*", table = "Resources", where = "Location = 'Brodie'"))
    return render_template('pages/gym.html', data=brodie_resources)


@app.route('/wilson')
def wilson():
    return render_template('pages/wilson.html')

@app.route('/wilsonEquipment')
def wilsonGym():
    if 'usr' not in session:
        print("\nNot logged in...")
    else:
        print("\nUser is logged in...")
        print("Email:", session['email'])
    wilson_resources = []
    wilson_resources.append("Wilson Equipment")
    wilson_resources.append(get_data.get_filtered_data(
        db, "*", table = "Resources", where = "Location = 'Wilson'"))
    return render_template('pages/gym.html', data=wilson_resources)


@app.route('/about')
def about():
    # query  = 'insert into User values (3, %s )' % "'superman'"
    # db.engine.execute(query)
    # r = db.engine.execute('select * from User')
    # s = ""
    # for i in r:
    #     s += i['name'] # This works if we wanna use a dict format, and tuples also work.
    return render_template('pages/placeholder.about.html')


@app.route('/profile')
def profile():
    if 'usr' not in session:
        print("\nNot logged in...")
        form = RegisterForm(request.form)
        return render_template('forms/login.html', form=form)
    else:
        print("\nUser is logged in...")
        print("Email:", session['email'])
    return render_template('pages/profile.html', userEmail=current_user['user']['email'], userDisplayName=current_user['user']['displayName'])


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def signUpCompleted():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpass = request.form.get('confirm')
        if password != confirmpass:
            form = RegisterForm(request.form)
            return render_template('forms/register.html', form=form)
        user = auth.create_user_with_email_and_password(email, password)
        #TODO: for protecting routes
        user_id = user['idToken']
        session['usr'] = user_id
        user_email = user['email'] if user is not None else None
        session['email'] = user_email
        # print(session)
        current_user['user'] = user
    return render_template('pages/placeholder.home.html', userInfo=user['idToken'])


@app.route('/login', methods=["GET", "POST"])
def signInCompleted():
    if request.method == "POST":
        email = request.form.get('name')
        password = request.form.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        #TODO: for protecting routes
        user_id = user['idToken'] if user is not None else None
        user_email = user['email'] if user is not None else None
        session['usr'] = user_id
        session['email'] = user_email
        # print(session)
        current_user['user'] = user
        jsonify(current_user['user'])
        # user = auth.refresh(user['refreshToken'])
        # print(user)
        if user == None:
            form = RegisterForm(request.form)
            return render_template('forms/login.html', form=form)
    return render_template('pages/placeholder.home.html', userInfo=user)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.route('/book_available_times/<ResourceID>', methods = ['GET', 'POST'])
def book_available_times(ResourceID = "0"):
    #print("reached")
    if request.method == "POST":
        dateTime = request.form.get('time').split(",")
        date, time = dateTime[0], dateTime[1] 
        #print(time)
        resType = request.form.get('resType')
        valuesDict = {'UserID': "23", 'DateBookedOn':date, 'TimeBookedAt':time, 'ResourceID':ResourceID, 'ResourceType':resType}
        process_data.insert_into_bookings(db, valuesDict)
        previous_url = request.referrer
        return redirect(previous_url)

    # for GET requests
    where = "ResourceID = {}".format(ResourceID)
    datesBooked = get_data.get_filtered_data(db, "DateBookedOn, TimeBookedAt", "Bookings", where)
    ret = process_data.get_available_datetimes(datesBooked, "08:00:00", "22:00:00")
    #print(ret)
    return ret

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
