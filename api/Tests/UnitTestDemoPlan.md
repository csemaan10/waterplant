# Unit Test Demo Test Plan
## Group number: L2-G5
## Date: April 4, 2023

## Tests Shown in Demo

### Test 1: Hardware - Moisture Sensor Tests (Christopher)

- testLowMoisture(): Hold moistsure sensor in open air and get moisture value. Assert moisture > 520
- testHighMoisture(): Place moistsure sensor in water and get moisture value. Assert moisture < 350

### Test 2: Software - Irrigation System Tests (Nicolas)

- testAboveMoistureThreshold(): Simulate sensor data by passing in a moisture value above the threshold 3 times. Assert pump does not turn on.
- testPassesMoistureThreshold(): Simulate sensor data by first passing in a moisture value above the threshold then one below the threshold. Assert pump turns on the second time.

### Test 3: Software - Graphical User Interface Test (Ismael)

displayData Test: Run a script to update the moisture, temperature, and humidity values in the database. Verify new values are displayed on the GUI.

## All Available tests

### Hardware Tests

1. Moisture Sensor Tests
  - testLowMoisture(): Hold moistsure sensor in open air and get moisture value. Assert moisture > 520
  - testHighMoisture(): Place moistsure sensor in water and get moisture value. Assert moisture < 350
2. Water Level Sensor Tests
  - testLowWaterLevel(): Hold water level sensor in open air and get sensor value. Assert value = 0
  - testHighWaterLevel(): Place water level sensor in water and get sensor value. Assert value > 80
3. Water Pump Test
  - testWaterPumps(): Turns each pump on and off, one at a time. Manually verify pumps are turned on
4. Servo Motor Test
  - testServo(): Turn servo to position 1, then 2, then 3 and verify the final position of the servo
5. SenseHat Tests
  - testTemp(): Measure current temperature value, assert value is between 20.0 and 50.0
  - testHumidity(): Measure current humidity, assert value is between 15.0 and 25.0

### Software Tests

1. Irrigation System Tests
  - testAboveMoistureThreshold(): Simulate sensor data by passing in a moisture value above the threshold 3 times. Assert pump does not turn on
  - testPassesMoistureThreshold():Simulate sensor data by first passing in a moisture value above the threshold then one below the threshold. Assert pump turns on the second time
2. Plant Environment Monitoring System Test
  - test_plantIDHealthy(): Passes in an image of a healthy plant to the PlantID API and verifies that it returns a healthy status
  - test_plantIDNotHealthy(): Passes in an image of a diseased plant to the PlantID API and verifies that it returns a diseased status
3. Email Notification Tests
  - test_lowWaterNotification(): Send low water notification email. Manually verify email was received
  - test_diseaseNotification(): Send potential disease notification email. Manually verify email was received
4. Graphical User Interface Tests
  - test_createUser(): Run the create user method and verify that the user information was properly stored in the database
  - test_registerPlant(): Run the register plant method and verify that the user information was properly stored in the database
  - displayData Test: Run a script to update the moisture, temperature, and humidity values in the database. Verify new values are displayed on the GUI
  - viewPlant Test: Click view plant button. Verify that livestream is started on GUI and plant is shown
