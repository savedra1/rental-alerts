import smtplib
import requests
import json
from aws_utils import AWSUtils

# Email configuration
def send_email(listings: str) -> None:
    sender_email = ""
    receiver_email = ""
    subject = "Subject of the email"
    body = "Body of the email"

    smtp_server = "smtp.gmail.com"
    smtp_username = ""
    smtp_password = ""

    message = f"Subject: {subject}\n\n{listings}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, receiver_email, message)
    server.close()

def send_email_atlassian_server(listings) -> int:
    response = requests.post(
        AWSUtils().get_api_password('atlassian/email_id'),
        headers = {
            "Content-Type": "application/json"
        },
        data = json.dumps({
            'listings': listings
        })
    )
    return response.status_code