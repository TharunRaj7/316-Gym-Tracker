def remove_reservation(db, type, itemID, userID = 0):
    query = ""
    if type == "Equip":
        query = "delete from Bookings where BookingID = {}".format(itemID)

    elif type == "Class":
        query = "delete from Enrollments where ClassID = {classID} and UserID = {userID}".format(classID = itemID, userID = userID)
    print(query)
    db.engine.execute(query)