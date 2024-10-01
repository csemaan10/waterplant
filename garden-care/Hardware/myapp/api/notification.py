import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

import pyrebase

config = {
  'apiKey': "AIzaSyD8uOQuCPAPX-IJkhnpop317MW02WXaMMs",
  'authDomain': "gardencare-bff9e.firebaseapp.com",
  'databaseURL': "https://gardencare-bff9e-default-rtdb.firebaseio.com",
  'projectId': "gardencare-bff9e",
  'storageBucket': "gardencare-bff9e.appspot.com",
  'messagingSenderId': "745509722354",
  'appId': "1:745509722354:web:73ace53e738116059e586b"
}

db = pyrebase.initialize_app(config).database()


def send_email(email_recipient,
               email_subject,
               email_message,
               attachment_location = ''):
    '''
    Send email template function
    Parameters:
    emailrecipient (string)
    email_subject (string)
    email_message (string)
    attachment_location (string)
    '''
    email_sender = 'gardencareL2G5@outlook.com'

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'plain'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.login('gardencareL2G5@outlook.com', 'plantid5')
    text = msg.as_string()
    server.sendmail(email_sender, email_recipient, text)
    print('email sent')
    server.quit()

    return True


def lowWaterNotification(name, email):
    '''
    Function with template for low water level email
    Parameters:
    name (string)
    email (string)
    '''

    subject = "WARNING: WATER LEVEL IS LOW"
    message = "Hello " + name + "\nThe water level for your Garden-Care system is running low!"
    message += "\nPlease refill the water tank."

    send_email(email, subject, message)


def diseaseNotification(name, email, plantID, disease):
    '''
    Function with template for disease identification email
    Parameters:
    name (string)
    email (string)
    plantID (int)
    disease (string)
    '''

    subject = "WARNING: POTENTIAL DISEASE DETECTED"
    message = "Hello " + name + "\nA potential disease has been found in one of the plants in your Garden-Care system"
    message += "\nPlant number: " + str(plantID)
    message += "\nPotential Disease: " + disease

    send_email(email, subject, message)
