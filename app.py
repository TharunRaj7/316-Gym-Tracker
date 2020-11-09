#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, current_app
from flask_sqlalchemy import SQLAlchemy
from backend_requests import get_data
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from data.insert_resources import insertRes
import pyrebase

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
    all_resources = get_data.get_all_resources(db)
    return render_template('pages/gym.html', data=all_resources)


@app.route('/brodie')
def brodieGym():
    brodie_resources = get_data.get_filtered_data(
        db, table = "Resources", where = "Location = 'Brodie'")
    return render_template('pages/gym.html', data=brodie_resources)


@app.route('/wilson')
def wilsonGym():
    wilson_resources = get_data.get_filtered_data(
        db, table = "Resources", where = "Location = 'Wilson'")
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
    return render_template('pages/placeholder.home.html', userInfo=user['idToken'])


@app.route('/login', methods=["GET", "POST"])
def signInCompleted():
    if request.method == "POST":
        email = request.form.get('name')
        password = request.form.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        print(user)
        if user == None:
            form = RegisterForm(request.form)
            return render_template('forms/login.html', form=form)
    return render_template('pages/placeholder.home.html')


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.route('/background_process_test/<ResourceID>')
def background_process_test(ResourceID):
    #print("reached")
    where = "ResourceID = {}".format(ResourceID)
    data = get_data.get_filtered_data(db, "Bookings", where)
    ret = {'dates':[]}
    for i in range(len(data)):
        row1 = data[i]
        date = row1['DateBookedOn'].strftime('%m/%d/%Y')
        ret['dates'].append(date)
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
