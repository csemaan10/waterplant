"""
The methods in this file are used to test if we can store our messages into
our database. When a user first visits out web interface, they will be
prompted to create an account with their name, username, password, email, and
notification preferences. That information will be passed into the createUser
method to create a user in the database and store the information. Once
complete, the user will be prompted to register a plant, with the information
for the plant name, moisture threashold, water threashold, and plant slot
number. This will be passed into the registerPlant method, along with their
userID, to be stored in the database under their user ID. The methods
test_createUser() and register_plant() simulate this process, and verify
that the passed in information has been stored properly in the database.
"""

import pyrebase

config = {
  'apiKey': "AIzaSyD8uOQuCPAPX-IJkhnpop317MW02WXaMMs",
  'authDomain': "gardencare-bff9e.firebaseapp.com",
  'databaseURL': "https://gardencare-bff9e-default-rtdb.firebaseio.com",
  'projectId': "gardencare-bff9e",
  'storageBucket': "gardencare-bff9e.appspot.com",
  'messagingSenderId': "745509722354",
  'appId': "1:745509722354:web:73ace53e738116059e586b"
}

db = pyrebase.initialize_app(config).database()

UT = "UserTable"
PT = "PlantTable"
MT = "Moisture Threashold"


def createUser(name: str, username: str, password: str,
               email: str) -> int:

    """Creates a new userID and stores the user's passed in information
    into the database under the User Table

    Keyword arguments:
    name (str)      -- The user's name
    username(str)   -- The user's username for their account
    password (str)  -- The user's password for their account
    email (str)     -- The user's email

    Return:
    userID (int)    -- The newly created ID for the user
    """

    # Get last user ID from database and increase by 1 to create new user ID
    userID_list = db.child(UT).get()
    userID = int(userID_list.val().popitem(True)[0]) + 1

    db.child(UT).child(userID).child("Name").set(name)
    db.child(UT).child(userID).child("Username").set(username)
    db.child(UT).child(userID).child("Password").set(password)
    db.child(UT).child(userID).child("Email").set(email)

    return userID


def registerPlant(userID: int, slot_num: int, name: str,
                  moisture_threas: int):

    """Registers a new plant and stores the passed in information in the
    database under the Plant Table

    Keyword arguments:
    userID (int)                -- The user's ID
    slotNum (int)               -- The slot the plant is placed in (from 1-4)
    name (str)                  -- The name of the plant
    moisture_threas (int)       -- The threashold to monitor for the moisture
    """

    db.child(PT).child(userID).child(slot_num).child("Name").set(name)
    db.child(PT).child(userID).child(slot_num).child(MT).set(moisture_threas)


def test_createUser():

    """Test for the createUser method. Simulates input from a user, calls
    createUser with the data, and verifies that the data was correctly
    stored in the database
    """

    name = "TestUser3"
    username = "TestUser3"
    password = "Password"
    email = "Test3@gmail.com"
    notify = True

    userID = createUser(name, username, password, email)

    db_name = db.child(UT).child(userID).child("Name").get().val()
    db_username = db.child(UT).child(userID).child("Username").get().val()
    db_password = db.child(UT).child(userID).child("Password").get().val()
    db_email = db.child(UT).child(userID).child("Email").get().val()
    db_notify = db.child(UT).child(userID).child("Notifications").get().val()

    input_message = [name, username, password, email, notify]
    db_values = [db_name, db_username, db_password, db_email, db_notify]
    assert (input_message == db_values)


def test_registerPlant():

    """Test for the registerPlant method. Simulates input from a user,
    calls registerPlant with the data, and verifies that the data was
    correctly store in the database
    """

    slot_num = 1
    input_name = "Plant1"
    moisture_threas = 0.70
    water_threas = 25

    # Get latest userID in database
    userID_list = db.child(UT).get()
    userID = int(userID_list.val().popitem(True)[0])

    registerPlant(userID, slot_num, input_name, moisture_threas, water_threas)

    name = db.child(PT).child(userID).child(slot_num).child("Name").get().val()
    db_moist = db.child(PT).child(userID).child(slot_num).child(MT).get().val()
    db_water_threas = db.child(PT).child(userID).child(WT).get().val()

    input_message = [input_name, moisture_threas, water_threas]
    db_values = [name, db_moist, db_water_threas]
    assert (input_message == db_values)


test_createUser()
test_registerPlant()

"""
Output of Flake8 linter returns no errors
"""
