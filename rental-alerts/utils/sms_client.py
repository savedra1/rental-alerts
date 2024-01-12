from twilio.rest import Client
from utils.aws_utils import AWSUtils

def send_sms(msg: str) -> str:
  awsu = AWSUtils()
  account_sid = awsu.get_parameter('/twilio/sid')
  auth_token = awsu.get_parameter('/twilio/auth_key')
  if account_sid == 'n/a' or auth_token == 'n/a':
    return 'Twilio not configured for project.'
  
  try:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
      from_=awsu.get_parameter('/twilio/sender'),
      to=awsu.get_parameter('/twilio/recipient'),
      body=msg 
    )

    return message.sid
  
  except Exception as err:
    return err

