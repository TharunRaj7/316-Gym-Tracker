import pandas as pd
from faker import Faker 
from collections import defaultdict
from sqlalchemy import create_engine
import pyodbc
import random

#random.choice(get_all_users)

def get_all_resourceIDs(db):
    query = 'select ResourceID from Resources;'
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    r = get_dict_from_result(db_result)
    return r

def get_all_users(db):
    query = 'select ID from User;'
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    r = get_dict_from_result(db_result)
    return r

def get_dict_from_result(db_result):
    list = []
    for i in db_result:
        list.append(i)
    return list


if __name__ == '__main__':

    fake = Faker() 
    print(fake.name())
    print(fake.future_date())
    #print(random.choice(get_all_users(??))

    #Enrollment Dictionary 
    #enrollments_fake["ClassID"].append(random.choice(get_all_users))
    #enrollments_fake["ClassDate"].append(print(fake.future_date()))

    #Bookings Dictionary


