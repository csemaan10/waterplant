from gpiozero import Servo
from time import sleep
from picamera import PiCamera
import base64
import os
import requests

# Initialize path for images
absolute_path = os.path.dirname(__file__)
print(absolute_path)
relative_path = "Images/"
full_path = os.path.join(absolute_path, relative_path)

# Initialize camera settings
camera = PiCamera()

camera.resolution = (1920, 1080)
camera.framerate = 15

class piCam:


    def turnServo(self, state: int):
        '''Turn Servo by position amount from origin and returns final position
        Parameters: state (int): position to reach
        '''
        servo = Servo(17)
        currPosition = 0
        if state == 1:
            position = -0.5
        elif state == 2:
            position = 0
        else:
            position = 0.5

        while True:
            servo.value = currPosition
            sleep(0.1)
            currPosition += 0.1
            print(currPosition)
            if currPosition >= position:
                return currPosition


    def captureImage(self):
        '''Captures image from Picam and returns encoded image
        Returns encoded Image
        '''
        camera.start_preview()
        sleep(0.5)
        camera.capture(full_path + 'test.jpg')
        camera.stop_preview()

        with open(full_path + "test.jpg", "rb") as img_file:
            encodedImage = base64.b64encode(img_file.read()).decode("ascii")
        
        return encodedImage

    def plantID(self):
        '''
        Send request to Plant.id API
        Returns list for plant indentification, disease status and disease name (strings)
        '''
        headers = {
        "Content-Type": "application/json",
        "Api-Key": "FYCY3Xsddr816VuqueuJ3VdNkyIv0jgjmU5LjbLATJmCPquvWl",
        }
        encodedImage = self.captureImage()
        id = requests.post('https://api.plant.id/v2/identify', json={'images': [encodedImage]}, headers = headers)
        print(id)
        identify = id.json()['suggestions'][0]['plant_name']
        diseaseResponse = requests.post('https://api.plant.id/v2/health_assessment', json={'images': [encodedImage]}, headers = headers)
        diseaseBool = diseaseResponse.json()['health_assessment']['is_healthy']
        if diseaseBool:
            diseaseName = "No Disease"
        else:
            diseaseName = diseaseResponse.json()['health_assessment']['diseases'][1]['name']
        return identify, diseaseBool, diseaseName
