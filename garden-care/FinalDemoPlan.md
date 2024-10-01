# Unit Test Demo Test Plan
## Group number: L2-G5
## Date: April 11, 2023

## Required Elements Checklist

1. One computer per group -> RPi running hardware, RPi running web server, Arduino, Phone/computer accesing GUI
2. One computer in headless mode -> RPi running web server
3. One hardware device per student -> water pumps (actuator), moisture sensor (sensor), water sensor
4. Actuator -> 4 water pumps
5. Feedback loop -> Moisture sensor reads value, if low water pump dispenses water, moisture sensor gets new value and loops if needed
6. Database with 2 tables. Hosting computer has other responsibilities -> Firebase contains User Table and Plant Table. Local SQL database on hardware RPi which handles the irrigation system as well
7. Periodic timing loop -> Checks moisture levels, waters plants, and gets temperature/humidity every 2 hours
8. Processing or analysis of IoT data read -> The information collected by the sensors will be displayed on the web GUI in real time for the user to see
9. Notifications -> Low water and plant health notifications
10. GUI -> Hosted on RPi running web server

## Functional Requirements from Detailed Design Doc

1. Plant Environment Monitoring: The system shall measure and record the soil moisture of each registered plant (up to 4), as well as the temperature and humidity every 2 hours. The data will be displayed for the user on a web graphical user interface. 

2. Automatic Irrigation: The system shall water a plant when the moisture of its soil is below the threshold. The user will be able to set a moisture threshold for when the water should be dispensed.

3. Water Level Notifications: The system shall send the user notifications to their email whenever the water level in the water tank is below a user set value, notifying them that the water needs to be refilled.  

4. Disease Identification: The system shall take a picture of each plant once a day and check for potential diseases using a disease identification Application Programming Interface (API). In the event of a potential disease, the system shall send the user a notification. 

5. Camera Livestream: The system shall start a camera livestream whenever requested by a user and be displayed on the web interface. 

6. Motion Detection: The system shall monitor the plants with a motion detection system for any potential animals approaching. Upon detection a flashing alarm will go off to scare the animal away. 
