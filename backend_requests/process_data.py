from datetime import datetime, timedelta
from collections import defaultdict
    
# Function to return available dates (for 2 days) for booking a specific resource
# From the database, time is passed as a Time object and data is passed as a Date object. Necessary conversions needed to work with DateTime
def get_available_datetimes(bookedDateTimes, gymStartTime, gymEndTime):
    startTime = datetime.strptime(gymStartTime, "%H:%M:%S").hour
    endTime = datetime.strptime(gymEndTime, "%H:%M:%S").hour

    # dates for today and the next day
    currentHour = datetime.now().time().hour
    currentDate = datetime.today().date()
    nextDate = currentDate + timedelta(days=1)
    
    all_times = [datetime.strptime(str(hour) + ":00:00", "%H:%M:%S").time() for hour in range(startTime, endTime)]
    
    # all times for 2 days that are booked
    dateTimeBookedDict = defaultdict(list)
    for item in bookedDateTimes:
        date = item["DateBookedOn"]
        time = datetime.strptime("00:00:00", "%H:%M:%S") + item["TimeBookedAt"]
        dateTimeBookedDict[date].append(time)
    #print(dateTimeBookedDict)    

    ret = {}
    timesNotAvailTod = [time.time() for time in dateTimeBookedDict[currentDate]]
    timesNotAvailTmrw = [time.time() for time in dateTimeBookedDict[nextDate]]
    ret[currentDate.strftime('%d %B %Y')] = [time.strftime("%I:%M %p") for time in all_times if (time not in timesNotAvailTod and time.hour > currentHour)]
    ret[nextDate.strftime('%d %B %Y')] = [time.strftime("%I:%M %p") for time in all_times if time not in timesNotAvailTmrw]

    # This returns a dict with keys as dates and values as a list of available times
    return ret


if __name__ == '__main__':
    data = [{"DateBookedOn" : datetime.strptime("11/05/2020", "%m/%d/%Y"), "TimeBookedAt" : datetime.strptime("11:00:00", "%H:%M:%S")}, 
    {"DateBookedOn" : datetime.strptime("11/12/2020", "%m/%d/%Y"), "TimeBookedAt" : datetime.strptime("15:00:00", "%H:%M:%S")},
    {"DateBookedOn" : datetime.strptime("11/12/2020", "%m/%d/%Y"), "TimeBookedAt" : datetime.strptime("10:00:00", "%H:%M:%S")}]
    
    print(get_available_datetimes(data, "08:00:00", "22:00:00"))