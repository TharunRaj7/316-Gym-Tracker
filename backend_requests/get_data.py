from datetime import datetime, timedelta

def get_all_resources(db):
    query = 'select * from Resources where ResourceDisplay = 1'
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    r = get_dict_from_result(db_result)
    return r


def get_all_classes(db):
    query = 'select * from ClassSchedule where EnrollmentCap > 0 AND ClassDisplay = 1'
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    r = get_dict_from_result(db_result)
    return r
    

def get_filtered_classes(db, filter_on, filter_val):
    """
    Takes in db engine, column to filter on, value to filter to
    (select * from resources where filter_on = 'filter_val')
    """
    query = "select * from ClassSchedule where {} = {} AND EnrollmentCap > 0 AND ClassDisplay = 1".format(
        filter_on, "'" + filter_val + "'")
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    r = get_dict_from_result(db_result)
    for item in r:
        item['ClassTime'] = (datetime.strptime("00:00:00", "%H:%M:%S") + item['ClassTime']).strftime("%I:%M %p")
    return r

def get_user_bookings_for_profile(db, userID):
    select = "B.ResourceID, R.ResourceName, B.ResourceType, R.Location, B.DateBookedOn, B.TimeBookedAt, B.BookingID"
    table = "Bookings B, Resources R"
    where = "R.ResourceID = B.ResourceID and B.UserID = {} order by B.DateBookedOn, B.TimeBookedAt".format(userID)
    data = get_filtered_data(db, select, table, where)
    for item in data:
        item['DateBookedOn'] = item['DateBookedOn'].strftime("%Y-%m-%d")
        time = datetime.strptime("00:00:00", "%H:%M:%S") + item["TimeBookedAt"]
        item['TimeBookedAt'] = time.strftime("%I:%M %p")
    return data

def get_user_enrollments_for_profile(db, userID):
    select = "E.ClassID, C.ClassDay, C.ClassDate, C.ClassType, C.ClassTime, C.ClassLocation, C.EnrollmentCap"
    table = "ClassSchedule C, Enrollments E"
    where = "C.ClassID = E.ClassID and E.UserID = {} order by C.ClassDate, C.ClassTime".format(userID)
    data = get_filtered_data(db, select, table, where)
    for item in data:
        item['ClassDate'] = item['ClassDate'].strftime("%Y-%m-%d")
        time = datetime.strptime("00:00:00", "%H:%M:%S") + item["ClassTime"]
        item['ClassTime'] = time.strftime("%I:%M %p")
    return data


def get_user_from_email(db, user_email):
    """
    Once User signs in, we use this function to get User ID/record from email
    """
    print("Getting user for email {}...".format(user_email))
    query = "select * from User where Email='{}'".format(user_email)
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    results_dict_list = get_dict_from_result(db_result)
    if not results_dict_list:  # no records matched
        return None
    # I return only the first [0] record from select *
    # Since hopefully emails are unique, there should be only 1 anyway
    return results_dict_list[0]


def get_all_users(db):
    """
    Gets us all the records in the User table
    """
    query = "select * from User;"
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    r = get_dict_from_result(db_result)
    return r

#General Utility function to retrieve data from the database
def get_filtered_data(db, select, table, where):
    query = "select {} from {} where {}".format(
        select, table, where)
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    r = get_dict_from_result(db_result)
    return r

def get_dict_from_result(db_result):
    """
    Returns a list of dictionaries where each dictionary is {field:value} pairs for one row.
    """
    d, a = {}, []
    
    for rowproxy in db_result:
        # rowproxy.items() returns an array like [(field0, value0), (field1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)
    return a

def no_where_get_filtered_data(db, select, table):
    query = "select {} from {}".format(
        select, table)
    db.engine.execute(query)
    db_result = db.engine.execute(query)
    r = get_dict_from_result(db_result)
    return r

