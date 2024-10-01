from flask import Flask, jsonify, request
from flask_cors import CORS
from .picam import piCam
from .planthealth import plantHealth
from .watering import waterSystem
from .constants import *
import requests
import json
import sqlite3
from time import sleep
from .notification import send_email, lowWaterNotification, diseaseNotification
import threading


app = Flask(__name__)
CORS(app)

# Hardware component initialization
camSystem = piCam()
sensorSystem = plantHealth()
wateringSystem = waterSystem()

dbconnect = sqlite3.connect("api/local.db", check_same_thread=False)
cursor = dbconnect.cursor()


@app.route('/')
def index():
    return "null"


@app.route('/pumpsON', methods = ['POST'])
def waterPlant():
    '''
    Endpoint function to activate pump returns sensor JSON
    '''
    pumpTime = request.json('pumpTime')
    plantID = request.json['plantID']
    wateringSystem.activatePump(pumpTime, plantID)
    sensorUpdate = sensorDump()
    return sensorUpdate


@app.route('/captureImage', methods = ['POST'])
def captureImage():
    '''
    Endpoint that captures image and returns encoded image
    '''
    image = camSystem.captureImage()
    return jsonify({"EncodedImage": image})


@app.route('/plantID', methods = ['POST'])
def requestplantID():
    '''
    Endpoints that gets plantID request and returns plant ID response JSON
    '''
    identify, diseaseBool, diseaseName = camSystem.plantID()
    return jsonify({"plantName": identify, "is_healthy": diseaseBool, "diseaseName": diseaseName})


@app.route('/userRegister', methods = ['POST'])
def userRegister():
    '''
    Endpoint to update user information
    '''
    global userID
    global name
    global email

    cursor.execute('''CREATE TABLE IF NOT EXISTS UserData(userID INTEGER, name STRING, email STRING)''')
    dbconnect.commit()

    userID = request.json['userID']
    name = request.json['name']
    email = request.json['email']

    cursor.execute('INSERT INTO UserData VALUES(?, ?, ?)', (userID, name, email))
    dbconnect.commit()

    return "500"


@app.route('/plantRegister', methods = ['POST'])
def plantRegister():
    '''
    Endpoint to update plant information
    '''

    cursor.execute('''CREATE TABLE IF NOT EXISTS PlantData(plantID INTEGER, moistureThreshold INTEGER)''')
    dbconnect.commit()

    plantID = request.json['plantID']
    moistureThreshold = request.json['moistureThreshold']

    cursor.execute('INSERT INTO PlantData VALUES(?, ?)', (plantID, moistureThreshold))
    dbconnect.commit()
    return "500"


@app.route('/updateSensorData', methods = ['POST'])
def sensorDump():
    '''
    endpoint to manually call sesnsor(unused)
    Returns sensor information JSON
    '''
    plantID = request.json('plantID') 
    moisture = sensorSystem.getMoisture(plantID)
    water = sensorSystem.getWaterLevel()
    temp, humidity = sensorSystem.getSense()

    sensorData = {
        "plantID": plantID,
        "Moisture": moisture,
        "WaterLevel": water,
        "Temperature": temp,
        "Humidity": humidity
    }
    return jsonify(sensorData)


def run_app():
    '''
    Method to run flask app as a thread
    '''
    app.run(debug=False, threaded=True)


def updateSensorDB(plantID):
    '''
    Local function to retrieve plant specific information
    plantID (int)
    Returns sensor data (dict)
    ''' 
    moisture = sensorSystem.getMoisture(plantID)
    water = sensorSystem.getWaterLevel()
    temp, humidity = sensorSystem.getSense()

    sensorData = {
        "userID": userID,
        "plantID": plantID,
        "Moisture": moisture,
        "WaterLevel": water,
        "Temperature": temp,
        "Humidity": humidity
    }

    return sensorData

  
def createLocalDB():
    '''
    Initializes local database tables
    '''
    cursor.execute('''CREATE TABLE IF NOT EXISTS UserData(userID INTEGER, name STRING, email STRING)''')
    dbconnect.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS PlantData(plantID INTEGER, moistureThreshold INTEGER)''')
    dbconnect.commit()


def initializeLocalDB():
    '''
    Initializes user information and default plant information for local DB
    '''
    global name
    global email

    res = requests.post(HARDWARE_IP+':5000/userInfo', json={'userID':userID})
    name = res.json()['name']
    email = res.json()['email']

    cursor.execute('INSERT INTO UserData VALUES(?, ?, ?)', (userID, name, email))
    dbconnect.commit()
    for i in range(1, 5):
        moistureThreshold = 1000
        cursor.execute('INSERT INTO PlantData VALUES(?, ?)', (i, moistureThreshold))
        dbconnect.commit()


def waterLoop(plantID, testMode = 0, testMoisture = 0, testThreshold = 0):
    '''
    Function to check if plant needs watering or water level empty
    Parameters:
    plantID (int)
    testMode (int)
    testMoisture (int)
    testThreshold (int)
    '''

    # Test Mode: 0 = normal, 1 = Test mode

    if testMode == 0:
        moisture = sensorSystem.getMoisture(plantID)
        waterLevel = sensorSystem.getWaterLevel()

        ThresholdDict = cursor.execute('SELECT * FROM PlantData')
        rows = cursor.fetchall()


        moistureThreshold = rows[plantID-1][1]

        while moisture > moistureThreshold:
            # if no water, send notification
            if waterLevel == 0:
                print("sent email")
                lowWaterNotification(userID)
                break
            else:
                wateringSystem.activatePump(0.5, plantID)
                systemActivated = True
                sleep(1)
                print(plantID)

                moisture = sensorSystem.getMoisture(plantID)

    # Test mode loop
    else:
        moisture = testMoisture
        waterLevel = 1000
        moistureThreshold = testThreshold

        systemActivated = False

        while moisture > moistureThreshold:

            if waterLevel == 0:
                print("sent email")
                lowWaterNotification(userID)
                break
            else:
                wateringSystem.activatePump(0.5, plantID)
                systemActivated = True
                sleep(1)

                print("Test mode: " + str(testMode))
                if testMode == 1:
                    break
                else:
                    moisture = sensorSystem.getMoisture(plantID)

        return systemActivated


def monitorSystem():
    '''
    Function to loop for plant watering and update sensors
    '''
    while True:
        for i in range(1, 5):
            waterLoop(i)

            plantName, diseaseStatus, diseaseName = camSystem.plantID()
            userIDDict = {
                "userID": userID,
                "plantID": i
            }
            plantIDResponse = {
                "plantName": plantName,
                "diseaseStatus": diseaseStatus,
                "diseaseName": diseaseName
            }

            sensorJSON = updateSensorDB(i)
            dbplantIDJSON = {**plantIDResponse, **userIDDict}

            print("loop " + str(i) + " done.")
            res = requests.post(HARDWARE_IP+':5000/addSensorData', json=sensorJSON)
            if res.ok:
                print(res.json())
            res = requests.post(HARDWARE_IP+':5000/updatePlantID', json=dbplantIDJSON)
            if res.ok:
                print(res.json())

        sleep(1000)


# Start up code for server
wateringSystem.pumpsOff()
userID = int(input("Enter userID: "))

createLocalDB()
initializeLocalDB()
first_thread = threading.Thread(target=run_app)
second_thread = threading.Thread(target=monitorSystem)
first_thread.start()
second_thread.start()
