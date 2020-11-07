import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

API_KEY = {
    "apiKey": "AIzaSyDjKfcd1yjSGG-seEnS_KNK8B6elIcFdKw",
    "authDomain": "final-bbbfc.firebaseapp.com",
    "databaseURL": "https://final-bbbfc.firebaseio.com",
    "projectId": "final-bbbfc",
    "storageBucket": "final-bbbfc.appspot.com",
    "messagingSenderId": "592348500050",
    "appId": "1:592348500050:web:098284b6ed5d530afecf8b",
    "measurementId": "G-TGJ2XYJB0Y"
}

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://sqlgods:=k}2gsJU9{Qv+h?W@vcm-16314.vm.duke.edu/GymReservation'
