
import json

import json
from time import sleep


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sender's email address and password
sender_email = "awsuser2213@gmail.com"
sender_password = "inlb qqcw ezqv udrv"

# Recipient's email address
recipient_email = "michaelsavedra@googlemail.com"

# Message details
subject = "Python Test"
body = "Sent from NixOS"

# Set up the MIMEText and MIMEMultipart objects
message = MIMEMultipart()
message.attach(MIMEText(body, 'plain'))
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email

# Establish a connection to the SMTP server
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()  # Start a secure connection
    server.login(sender_email, sender_password)  # Log in to the Gmail account

    # Send the email
    response = server.sendmail(sender_email, recipient_email, message.as_string())
    print(response)

print("Email sent successfully.")







