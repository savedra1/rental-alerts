
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



"""from playwright.sync_api import sync_playwright"""


"""url = 'https://www.zoopla.co.uk/to-rent/houses/london/?beds_max=2&price_frequency=per_month&price_max=600&property_sub_type=detached&property_sub_type=semi_detached&property_sub_type=terraced&q=London&radius=3&results_sort=newest_listings&search=to-rent'

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    page = context.new_page()
    page.goto(url)
    html_source = page.content()
    print(html_source)
    browser.close()"""


"""url = "https://www.zoopla.co.uk/to-rent/houses/london/?beds_max=2&price_frequency=per_month&price_max=600&property_sub_type=detached&property_sub_type=semi_detached&property_sub_type=terraced&q=London&radius=3&results_sort=newest_listings&search=to-rent"

apikey = '425c7f0e256f581278ea86502ac1045e62b92e56'
params = {
    'url': url,
    'apikey': apikey,
	'js_render': 'true',
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
print(response.text)"""





