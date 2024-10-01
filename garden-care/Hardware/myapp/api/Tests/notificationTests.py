
import sys

sys.path.append('../')

import planthealth
import picam
import watering
from notification import send_email, lowWaterNotification, diseaseNotification

def test_lowWaterNotification():

    name = "TEST USER"
    email = "christopherjsemaan@cmail.carleton.ca"

    lowWaterNotification(name, email)

def test_diseaseNotification():

    name = "TEST USER"
    email = "christopherjsemaan@cmail.carleton.ca"
    plantID = 1
    disease = "TEST DISEASE"

    diseaseNotification(name, email, plantID, disease)

def test_plantIDHealthy():
    camSystem = picam.piCam()
    diseaseResponse =camSystem.plantID()
    assert(diseaseResponse[1] == True)

def test_plantIDNotHealthy():
    camSystem = picam.piCam()
    diseaseResponse =camSystem.plantID()
    assert(diseaseResponse[2] != "No Disease")

test_lowWaterNotification()
test_diseaseNotification()
test_plantIDHealthy()