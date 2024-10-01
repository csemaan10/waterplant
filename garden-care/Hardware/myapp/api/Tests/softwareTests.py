
import sys
sys.path.append('../')
import watering
import planthealth
import sqlite3
import pandas
from time import sleep

from api import waterLoop
def testAboveMoistureThreshold():

    userID = 100
    plantID = 1
    testMode = 1
    moisture = 200
    moistureThreshold = 400

    systemActivated = waterLoop(plantID, testMode, moisture, moistureThreshold)
    assert(not systemActivated)
    systemActivated = waterLoop(plantID, testMode, moisture, moistureThreshold)
    assert(not systemActivated)
    systemActivated = waterLoop(plantID, testMode, moisture, moistureThreshold)
    assert(not systemActivated)

def testPassesMoistureThreshold():

    userID = 100
    plantID = 1
    testMode = 1
    moisture = 200
    moistureThreshold = 400

    systemActivated = waterLoop(plantID, testMode, moisture, moistureThreshold)
    assert(not systemActivated)

    moisture = 500

    systemActivated = waterLoop(plantID, testMode, moisture, moistureThreshold)
    assert(systemActivated)

testAboveMoistureThreshold()
testPassesMoistureThreshold()
