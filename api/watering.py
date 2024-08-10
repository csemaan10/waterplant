import RPi.GPIO as GPIO
import time


PUMP_PIN = [23, 24, 16, 27]
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_PIN[0], GPIO.OUT)
GPIO.setup(PUMP_PIN[1], GPIO.OUT)
GPIO.setup(PUMP_PIN[2], GPIO.OUT)
GPIO.setup(PUMP_PIN[3], GPIO.OUT)


class waterSystem:

    def activatePump(self, pumpTime: float, plantID):
        '''Turns on PUMP pin for pumpTime amount
        Parameters: pumpTime (float): amount off time for pump on
        '''
        GPIO.output(PUMP_PIN[plantID-1], GPIO.LOW)
        print("on")
        time.sleep(pumpTime)
        GPIO.output(PUMP_PIN[plantID-1], GPIO.HIGH)
        print("off")
        time.sleep(pumpTime)

    def pumpsOff(self):
        '''All pumps turn off'''
        GPIO.output(PUMP_PIN[0], GPIO.HIGH)
        GPIO.output(PUMP_PIN[1], GPIO.HIGH)
        GPIO.output(PUMP_PIN[2], GPIO.HIGH)
        GPIO.output(PUMP_PIN[3], GPIO.HIGH)
