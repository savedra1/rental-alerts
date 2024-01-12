import requests
import json
from utils.aws_utils import AWSUtils

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
def send_email(listings, subject="NEW LISTINGS ADDED") -> str:
    """This function requires a GMAIL email acocunt
        with an app password as auth. """
    
    awsu = AWSUtils()

    sender_email: str    = awsu.get_parameter('/smtp/sender_email')
    sender_password: str = awsu.get_parameter('/smtp/sender_key')
    recipient_email: str = awsu.get_parameter('/smtp/recipient_email')
    sub: str             = subject
    body: str            = listings

    try:
        message = MIMEMultipart()
        message.attach(MIMEText(body, 'plain'))
        message['Subject'] = sub
        message['From'] = sender_email
        message['To'] = recipient_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start a secure connection
            server.login(sender_email, sender_password)  # Log in to the Gmail account

            response = server.sendmail(sender_email, recipient_email, message.as_string())
            print(response)

        return "Email sent successfully."
    
    except Exception as err:
        return err


def send_email_atlassian_server(listings) -> int:
    """secondary method of ending an email utilising an atlassian AFJ"""
    response = requests.post(
        AWSUtils().get_parameter('atlassian/email_id'),
        headers = {
            "Content-Type": "application/json"
        },
        data = json.dumps({
            'listings': listings
        })
    )
    return response.status_code