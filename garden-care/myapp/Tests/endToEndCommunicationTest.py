import requests
import pyrebase
import json
import sys

sys.path.append('../')
from Hardware.Watering import waterPlant

moist1 = 0.1
moist_thres = 0.2
water_lev = 100
temp1 = 30
hum1 = 0.3
userID = 100
plantID = 1

#Database connection info
config = {
  'apiKey': "AIzaSyD8uOQuCPAPX-IJkhnpop317MW02WXaMMs",
  'authDomain': "gardencare-bff9e.firebaseapp.com",
  'databaseURL': "https://gardencare-bff9e-default-rtdb.firebaseio.com",
  'projectId': "gardencare-bff9e",
  'storageBucket': "gardencare-bff9e.appspot.com",
  'messagingSenderId': "745509722354",
  'appId': "1:745509722354:web:73ace53e738116059e586b"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# def test_RaspPiToFront():

def test_SendAndReceiveSensorDataDB():
    #Record current moisture, temperature, and humidity from sensors
    ## TO IMPLEMENT LATER

    res = requests.post('http://localhost:5000/addSensorData', json={"moisture":moist1, "temp": temp1, "humidity": hum1})
    if res.ok:
        print(res.json())

    db_moist = res.json()['Moisture'] 
    db_temp = res.json()['Temperature'] 
    db_hum = res.json()['Humidity'] 

    assert moist1 == db_moist

    assert temp1 == db_temp

    assert hum1 == db_hum

    print("Test Send and Receive to Database Passed")


def test_HardwaretoBackend():
    res2 = requests.post('http://localhost:5000/waterPlant', json={"Moisture":moist1, "WaterLevel": water_lev})
    if res2.ok:
        print(res2.json())
    assert res2.json() == {'Status': 'Done'}

    print("Test watering server to hardware Passed")

test_SendAndReceiveSensorDataDB()

test_HardwaretoBackend()

