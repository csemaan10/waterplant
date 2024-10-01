# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append('../')
import planthealth
import picam
import watering
import math
import json
from time import sleep

def testLowMoisture():
    p1 = planthealth.plantHealth()
    moisture = p1.getMoisture(1)
    assert(moisture>520)

def testHighMoisture():
    p1 = planthealth.plantHealth()
    moisture = p1.getMoisture(1)
    assert(moisture<350)

def testLowWaterLevel():
    p1 = planthealth.plantHealth()
    water = p1.getWaterLevel()
    print(water)
    assert(water==0)

def testHighWaterLevel():
    p1 = planthealth.plantHealth()
    water = p1.getWaterLevel()
    assert(water>80)

def testTemp():
    p1 = planthealth.plantHealth()
    temp, humidity = p1.getSense()
    assert(20.0<temp and 50.0 > temp)

def testHumidity():
    p1 = planthealth.plantHealth()
    temp, humidity = p1.getSense()
    assert(15.0<humidity and 25.0 > humidity)

def testServo():
    cam = picam.piCam()
    cam.turnServo(1)
    sleep(2)
    cam.turnServo(2)
    sleep(2)
    lastPosition = cam.turnServo(3)
    sleep(2)
    assert(lastPosition ==0.5)

def testWaterPumps():
    w = watering.waterSystem()
    w.activatePump(0.5, 1)
    w.activatePump(0.5, 2)
    w.activatePump(0.5, 3)
    w.activatePump(0.5, 4)


testLowMoisture()
# testLowWaterLevel()
testHighMoisture()
# testHighWaterLevel()
# testTemp()
# testHumidity()
# testWaterPumps()
# testServo()
