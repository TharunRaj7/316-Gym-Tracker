from datetime import datetime, timedelta
from collections import defaultdict
from backend_requests import get_data

# Function to return available dates (for 2 days) for booking a specific resource
# From the database, time is passed as a Time object and data is passed as a Date object. Necessary conversions needed to work with DateTime


def get_available_datetimes(bookedDateTimes, gymStartTime, gymEndTime):
    startTime = datetime.strptime(gymStartTime, "%H:%M:%S").hour
    endTime = datetime.strptime(gymEndTime, "%H:%M:%S").hour

    # dates for today and the next day
    currentHour = datetime.now().time().hour
    currentDate = datetime.today().date()
    nextDate = currentDate + timedelta(days=1)

    all_times = [datetime.strptime(
        str(hour) + ":00:00", "%H:%M:%S").time() for hour in range(startTime, endTime)]

    # all times for 2 days that are booked
    dateTimeBookedDict = defaultdict(list)
    for item in bookedDateTimes:
        date = item["DateBookedOn"]
        time = datetime.strptime("00:00:00", "%H:%M:%S") + item["TimeBookedAt"]
        dateTimeBookedDict[date].append(time)
    # print(dateTimeBookedDict)

    ret = {}
    timesNotAvailTod = [time.time()
                        for time in dateTimeBookedDict[currentDate]]
    timesNotAvailTmrw = [time.time() for time in dateTimeBookedDict[nextDate]]
    ret[currentDate.strftime('%d %B %Y')] = [time.strftime("%I:%M %p") for time in all_times if (
        time not in timesNotAvailTod and time.hour > currentHour)]
    ret[nextDate.strftime('%d %B %Y')] = [time.strftime("%I:%M %p")
                                          for time in all_times if time not in timesNotAvailTmrw]

    # This returns a dict with keys as dates and values as a list of available times
    return ret


def insert_into_bookings(db, valuesDict):
    date = datetime.strptime(
        valuesDict['DateBookedOn'], "%d %B %Y").strftime("%Y-%m-%d")
    time = datetime.strptime(
        valuesDict['TimeBookedAt'], "%I:%M %p").strftime("%H:%M:%S")
    query = "insert into Bookings (UserID, DateBookedOn, TimeBookedAt, ResourceID, ResourceType) values ("
    query += valuesDict['UserID'] + ",'" + date + "','" + time + "'," + \
        valuesDict['ResourceID'] + ",'" + valuesDict['ResourceType'] + "')"
    print(query)
    db.engine.execute(query)


def insert_into_enrollments(db, valuesDict):
    date = valuesDict['DateBookedOn']
    ClassID = valuesDict['ResourceID']
    Email = valuesDict['Email']
    UserInfo = get_data.get_user_from_email(db, Email)
    print(UserInfo)
    UserID = UserInfo['ID']
    print(UserID)
    query = "insert into Enrollments (UserID, ClassID, ClassDate) values (" + "{UserID}".format(
        UserID=UserID) + "," + ClassID + ", {date}".format(date=date) + ")"
    print(query)
    # db.engine.execute(query)
    # db.engine.execute(updateQuery)


# Make sure to wrap a string value with single quotes inside the double quotes
def insert_to_db(db, table, schema, values):
    query = "insert into {} (".format(table)
    for item in schema:
        query += item + ","
    query = query[:-1]
    query += ") values ("

    for val in values:
        query += val + ","
    query = query[:-1] + ");"
    db.engine.execute(query)
    # print(query)


def validate_username(user_name):
    """
    Ensures username is only alphabets. Called in signup function in app.py
    """
    return user_name.isalpha()


def insert_into_users(db, user_name, user_email):
    """
    Users: ID, Name, Email, AccountCreated
    We calculate AccountCreated in this function
    """
    account_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query_string = "insert into User (Name, Email, AccountCreated) values ("
    query_string += "'{name}', '{email}', '{accountcreated}');".format(
        name=user_name, email=user_email, accountcreated=account_created)
    print(query_string)
    db.engine.execute(query_string)


if __name__ == '__main__':
    data = [{"DateBookedOn": datetime.strptime("11/05/2020", "%m/%d/%Y"), "TimeBookedAt": datetime.strptime("11:00:00", "%H:%M:%S")},
            {"DateBookedOn": datetime.strptime(
                "11/12/2020", "%m/%d/%Y"), "TimeBookedAt": datetime.strptime("15:00:00", "%H:%M:%S")},
            {"DateBookedOn": datetime.strptime("11/12/2020", "%m/%d/%Y"), "TimeBookedAt": datetime.strptime("10:00:00", "%H:%M:%S")}]

    #print(get_available_datetimes(data, "08:00:00", "22:00:00"))

    table = "Bookings"
    schema = ["UserID, DateBookedOn, TimeBookedAt, ResourceID, ResourceType"]
    values = ["23", "'08/26/2020'", "'23:00:00'", "45", "'Equipment'"]

    insert_to_db("", table, schema, values)
