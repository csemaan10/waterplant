#!/usr/bin/env python3
import serial
from sense_hat import SenseHat

sense = SenseHat()


class plantHealth:

    def getMoisture(self, plantID):
        '''Gets moisture from arduino and returns moisture as int'''
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        while True:

            if ser.in_waiting > 0:
                arduinoData = ser.readline().decode().rstrip()
                arduinoData = arduinoData.split(",")

                return int(arduinoData[plantID])

    def getWaterLevel(self):
        '''Gets Water level from arduino and returns water level as int'''
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()

        while True:

            if ser.in_waiting > 0:
                arduinoData = ser.readline().decode().rstrip()
                arduinoData = arduinoData.split(",")
                return int(arduinoData[0])

    def getSense(self):
        '''Gets temperature and humidity from sensehat and returns float'''
        while True:
            temp = sense.get_temperature()
            humidity = sense.get_humidity()

            temp = round(temp, 1)
            humidity = round(humidity, 1)

            return temp, humidity
