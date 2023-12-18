from twilio.rest import Client

from aws_utils import AWSUtils
        

def send_sms(msg: str):# -> str:
  awsu = AWSUtils()
  account_sid = awsu.get_api_password('/twilio/sid')
  auth_token = awsu.get_api_password('/twilio/auth_key')

  client = Client(account_sid, auth_token)

  message = client.messages.create(
    from_=awsu.get_api_password('/twilio/sender'),
    to=awsu.get_api_password('/twilio/recipient'),
    body=msg 
  )

  return message.sid

