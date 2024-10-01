## @author Ismael Mfumu 
## @date March 29, 2029
## @class SYSC 3010
## @project Smart Plant Backend

## The purpose of this code is to configure the data from the database, to the
## hardware devices and the frontend tools. The frontend tools will be represented by 
## the HTML template and the hardware device will be operated by the Hardwareresponse
## parameter. The code below will show how the database is configured and the different 
## methods that will be used to transfer data between systems and manipulating both systems
## using the backend as a coordinator 

import subprocess
  
from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pyrebase
import json
import requests
from time import sleep

app = Flask(__name__)
CORS(app)


# Configures the backend data to the friebase realtime database

config = {
  'apiKey': "AIzaSyD8uOQuCPAPX-IJkhnpop317MW02WXaMMs",
  'authDomain': "gardencare-bff9e.firebaseapp.com",
  'databaseURL': "https://gardencare-bff9e-default-rtdb.firebaseio.com",
  'projectId': "gardencare-bff9e",
  'storageBucket': "gardencare-bff9e.appspot.com",
  'messagingSenderId': "745509722354",
  'appId': "1:745509722354:web:73ace53e738116059e586b"

}

# Initializing database 

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Global variables 
username = "blank"
email = "blank"
password = "blank"
name = "blank"
userID = "blank"

UT = "UserTable"
PL = "PlantTable"

plantNum = "blank"
plantName = "blank"
moistThreashold = "blank"

@app.route('/')
def index():
    return render_template('dashboard.html')

# Following code takes userID and plant data and adds temperature,
# humidity and pressures from Raspberry Pi and put it into HTML.
# Reurnds it back and prints it in backend

@app.route('/addSensorData', methods = ['POST'])
def addSensorData():

    reqUserID = request.json["userID"]
    plantID = request.json["plantID"]

    moisture_list = db.child("PlantTable").child(reqUserID).child(plantID).child("Moisture").get().each()
    temperature_list = db.child("PlantTable").child(reqUserID).child(plantID).child("Temperature").get().each()
    humidity_list = db.child("PlantTable").child(reqUserID).child(plantID).child("Humidity").get().each()

    moisture_list += [request.json["Moisture"]]
    temperature_list += [request.json["Temperature"]]
    humidity_list += [request.json["Humidity"]]

    moisture_list = moisture_list[-10:]
    temperature_list = temperature_list[-10:]
    humidity_list = humidity_list[-10:]

    for i in range(len(moisture_list) - 1):
        db.child("PlantTable").child(reqUserID).child(plantID).child("Moisture").child(i).set(moisture_list[i].val())
        db.child("PlantTable").child(reqUserID).child(plantID).child("Temperature").child(i).set(temperature_list[i].val())
        db.child("PlantTable").child(reqUserID).child(plantID).child("Humidity").child(i).set(humidity_list[i].val())
        
    db.child("PlantTable").child(reqUserID).child(plantID).child("Moisture").child(i + 1).set(moisture_list[len(moisture_list) - 1])
    db.child("PlantTable").child(reqUserID).child(plantID).child("Temperature").child(i + 1).set(temperature_list[len(moisture_list) - 1])
    db.child("PlantTable").child(reqUserID).child(plantID).child("Humidity").child(i + 1).set(humidity_list[len(moisture_list) - 1])

    db.child("PlantTable").child(reqUserID).child("WaterLevel").child(0).set(request.json["WaterLevel"])
    return "500"


@app.route('/updatePlantID', methods = ['POST'])
def updateplantID():
    reqUserID = request.json["userID"]
    plantID = request.json["plantID"]

    plantName = request.json["plantName"]
    diseaseStatus = request.json["diseaseStatus"]
    diseaseName = request.json["diseaseName"]

    db.child("PlantTable").child(reqUserID).child(plantID).child("Moisture").child("PlantName").set(plantName)
    db.child("PlantTable").child(reqUserID).child(plantID).child("Temperature").child("DiseaseStatus").set(diseaseStatus)
    db.child("PlantTable").child(reqUserID).child(plantID).child("Humidity").child("DiseaseName").set(diseaseName)
    
    return "500"

@app.route('/userInfo', methods = ['POST'])
def adduserInfo():
    reqUserID = request.json["userID"]

    email = db.child("UserTable").child(reqUserID).child("Email").get().val()
    name = db.child("UserTable").child(reqUserID).child("Name").get().val()

    return jsonify({"email":email, "name":name})


@app.route('/login', methods = ['POST', 'GET'])
def getLogin():
    if request.method == 'POST':
        
        user = request.form.get("uname")
        psw = request.form.get("psw")
        

        data = {
            "Username" : user,
            "Password" : psw
        }
        db.child('Users').child('Firstperson').update(data)
    
    return render_template('dashboard.html')
    

@app.route('/regU', methods = ['POST', 'GET'])
def createUser():

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

    #Getting values from db inputs
    if request.method == 'POST':
        
        global username 
        global email
        global password 
        global name
        global userID 
        
        username = request.form.get("newUsername")
        email = request.form.get("newEmail")
        password = request.form.get("newPassword")
        name = request.form.get("newName")
        userID = request.form.get("UID")
        
        # Setting UserID to same Values
        db.child(UT).child(userID).child("Name").set(name)
        db.child(UT).child(userID).child("Username").set(username)
        db.child(UT).child(userID).child("Password").set(password)
        db.child(UT).child(userID).child("Email").set(email)

    # Get plant names for display
    plantName1 = db.child("PlantTable").child(userID).child(1).child("Name").get().val()
    plantName2 = db.child("PlantTable").child(userID).child(2).child("Name").get().val()
    plantName3 = db.child("PlantTable").child(userID).child(3).child("Name").get().val()
    plantName4 = db.child("PlantTable").child(userID).child(4).child("Name").get().val()
    
    return render_template('second.html', name = name, username = username, userID = userID,
    plantName1 = plantName1, plantName2 = plantName2, plantName3 = plantName3, plantName4 = plantName4)


@app.route('/regP', methods = ['POST', 'GET'])
def registerPlant():

    global userID
    global plantNum
    global plantName 
    # Getting values from HTML
    plantNum = request.form.get("plantNum")
    plantName = request.form.get("plantName")
    moistThreashold = request.form.get("MT")
    
    # Set values into DB
    db.child("PlantTable").child(userID).child(plantNum).child("Name").set(plantName)
    db.child("PlantTable").child(userID).child(plantNum).child("MoistureThreshold").set(moistThreashold)
    db.child("PlantTable").child(userID).child(plantNum).child("HealthStatus").child("Diseases").set("N/A")
    db.child("PlantTable").child(userID).child(plantNum).child("HealthStatus").child("Healthy").set(True)

    for i in range(10):
        db.child("PlantTable").child(userID).child(plantNum).child("Moisture").child(i).set(0)
        db.child("PlantTable").child(userID).child(plantNum).child("Temperature").child(i).set(0)
        db.child("PlantTable").child(userID).child(plantNum).child("Humidity").child(i).set(0)
    
    plantName1 = db.child("PlantTable").child(userID).child(1).child("Name").get().val()
    plantName2 = db.child("PlantTable").child(userID).child(2).child("Name").get().val()
    plantName3 = db.child("PlantTable").child(userID).child(3).child("Name").get().val()
    plantName4 = db.child("PlantTable").child(userID).child(4).child("Name").get().val()
    
    # Setting new values to certain areas in HTML
    return render_template('second.html', name = name, username = username, userID = userID,
    plantName1 = plantName1, plantName2 = plantName2, plantName3 = plantName3, plantName4 = plantName4,
    health = db.child("PlantTable").child(userID).child(plantNum).child("HealthStatus").child("Healthy").get().val()
    )

@app.route('/viewPlants', methods = ['POST', 'GET'])
def viewPlants():

    if request.method == 'POST':
        
        global username 
        global email
        global password 
        global name
        global userID

        subprocess.run(["python", "api/livestream.py"])
        print("The method is running")

        plantName1 = db.child("PlantTable").child(userID).child(1).child("Name").get().val()
        plantName2 = db.child("PlantTable").child(userID).child(2).child("Name").get().val()
        plantName3 = db.child("PlantTable").child(userID).child(3).child("Name").get().val()
        plantName4 = db.child("PlantTable").child(userID).child(4).child("Name").get().val()

        return render_template('second.html', name = name, username = username, userID = userID,
    plantName1 = plantName1, plantName2 = plantName2, plantName3 = plantName3, plantName4 = plantName4)
    
@app.route('/armMotionDetection', methods = ['POST', 'GET'])
def armMotionDetection():

    """
    """
    print("ARM MOTION DETECTION")


if __name__ == '__main__':
    app.run(debug=True)
