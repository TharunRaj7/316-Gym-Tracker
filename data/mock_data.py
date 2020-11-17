from flask import Flask, render_template, request, current_app, session
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify
from backend_requests import get_data
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from data.insert_resources import insertRes
import pyrebase
import random
from faker import Faker 
from collections import defaultdict
from sqlalchemy import create_engine
import pandas as pd

sql_engine = create_engine('mysql://sqlgods:=k}2gsJU9{Qv+h?W@vcm-16314.vm.duke.edu/GymReservation', echo=False)

## START GENERATING BOOKINGS  ##
    fake = Faker() 
    Bookings_Dic = {"UserID":[],"DateBookedOn":[],"TimeBookedAt":[], "ResourceID":[], "ResourceType":[]}

    for x in range(100):

        #GET RANDOM RESOURCE ID + RESOURCE TYPE 
        a = get_data.no_where_get_filtered_data(db,"ResourceID, ResourceType", "Bookings")
        b = [[k["ResourceID"], k["ResourceType"]] for k in a]
        c = random.choice(b)
        ## c[0]= ResourceID c[1] = ResourceType 

        #GET SINGLE RANDOM USER 
        d = get_data.no_where_get_filtered_data(db,"ID", "User")
        e = []
        for i in d:
            for key, value in i.items():
                e.append(value)
        f = random.choice(e)

        #GET RANDOM TIME
        g = ["8:00:00", "9:00:00", "10:00:00", "11:00:00", "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00", "17:00:00", "18:00:00", 
        "19:00:00", "20:00:00", "21:00:00"]
        h = random.choice(g)

        #GET RANDOM DATE IN NEXT 2 WEEKS
        i = ["2020-11-18", "2020-11-19", "2020-11-20", "2020-11-21", "2020-11-22", "2020-11-23", "2020-11-24", "2020-11-25", "2020-11-26", "2020-11-27", "2020-11-28", 
        "2020-11-29", "2020-11-30", "2020-12-01", "2020-12-02", "2020-12-03", "2020-12-04"]
        j = random.choice(i)

        Bookings_Dic["UserID"].append(f)
        Bookings_Dic["DateBookedOn"].append(j)
        Bookings_Dic["TimeBookedAt"].append(h)
        Bookings_Dic["ResourceID"].append(c[0])
        Bookings_Dic["ResourceType"].append(c[1])

    output_Bookings = pd.DataFrame(Bookings_Dic)
    sql_engine = create_engine('mysql://sqlgods:=k}2gsJU9{Qv+h?W@vcm-16314.vm.duke.edu/GymReservation', echo=False)
    output_Bookings.to_sql("Bookings", sql_engine, if_exists='append', index=False, index_label=None, chunksize=None, dtype=None, method=None)



## START GENERATING ENROLLMENTS##

Enrollments_Dic = {"ClassID":[],"UserID":[],"ClassDate":[]}

for x in range(100):
    a = get_data.no_where_get_filtered_data(db,"ClassID, ClassDate", "ClassSchedule")
    b = [[k["ClassID"], k["ClassDate"]] for k in a]
    c = random.choice(b)

    d = get_data.no_where_get_filtered_data(db,"ID", "User")
    e = []
    for i in d:
        for key, value in i.items():
            e.append(value)
    f = random.choice(e)

    Enrollments_Dic["ClassID"].append(c[0])
    Enrollments_Dic["UserID"].append(f)
    Enrollments_Dic["ClassDate"].append(str(c[1]))


output_Enrollments = pd.DataFrame(Enrollments_Dic)
output_Enrollments.to_sql("User", sql_engine, if_exists='append', index=False, index_label=None, chunksize=None, dtype=None, method=None)

## END GENERATING FAKE ENROLLMENTS ##

## START GENERATING FAKE USERS ##


User_Dic = {"ID":[],"Name":[],"Email":[], "AccountCreated":[]}

abc = 113
for x in range(100):
    User_Dic["ID"].append(abc)
    User_Dic["Name"].append(fake.name())
    User_Dic["Email"].append(fake.email())
    User_Dic["AccountCreated"].append(fake.past_date())
    abc= abc+1

output_User = pd.DataFrame(User_Dic)
sql_engine = create_engine('mysql://sqlgods:=k}2gsJU9{Qv+h?W@vcm-16314.vm.duke.edu/GymReservation', echo=False)
output_User.to_sql("User", sql_engine, if_exists='append', index=False, index_label=None, chunksize=None, dtype=None, method=None)

## END GENERATING FAKE USERS ##

if __name__ == '__main__':