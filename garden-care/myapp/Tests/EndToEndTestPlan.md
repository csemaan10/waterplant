# End To End Communication Demo Test Plan
## Group number: L2-G5
## Date: March 14, 2023

### Test 1: Communication Between Frontend and Backend (Christopher)

Test to show communication exists between the front end web GUI and backend

### Test 2: test_SendAndReceiveSensorDataDB() (Ismael)

Test to show communication exists between backend and cloud database

  Dummy sensor data is sent from the backend to Firebase to be stored in the cloud database. Data is then taken from Firebase, sent back to the backend, and verified.

### Test 3: test_hardwareToBackend() (Nicolas)

Test to show communication exists between hardware and backend

  Backend sends a request to the hardware which returns the status. Backend then verifies that the hardware return status is "Done"
 

