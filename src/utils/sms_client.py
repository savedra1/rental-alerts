from twilio.rest import Client
import os

url = 'https://www.google.com'

def send_sms(msg: str):
  account_sid = os.getenv('TWILIO_SID')
  auth_token = os.getenv('TWILIO_AUTH_TOKEN')

  client = Client(account_sid, auth_token)

  message = client.messages.create(
    from_='+447588045860',
    to=os.getenv('MOBILE_NUM'),
    body = f'New listing: {msg}\nNew listing: {msg}\nNew listing: {msg}\nNew listing: {msg}\n'
  )

  print(message.sid)

if __name__ == "__main__":
  send_sms(url)