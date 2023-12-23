
import sys
import traceback

import json
from datetime import datetime

from scrapers.rightmove import Rightmove
#from scrapers.zoopla import Zoopla
from scrapers.on_the_market import OnTheMarket

import boto3

from utils.logger import set_up_logger, alert_admin
from utils.sms_client import send_sms
from utils.email_client import send_email, send_email_atlassian_server

def lambda_handler(event, context):
    function_response = {
        'statusCode': 200,
        'body': json.dumps({})
    }
    logger = set_up_logger()

    try:
        handler = LambdaHandler(event, context, logger)
        handler.run()

    except Exception as err:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(
            exception_type, exception_value, exception_traceback
        )
        err_msg = json.dumps( {
            'errorType': exception_type.__name__,
            'errorMessage': str(exception_value),
            'stackTrace': str(traceback_string)
        } )
        logger.error(err_msg)
        alert_admin(err_msg)
        function_response['statusCode'] = 500
        function_response['body'] = str(err)


class LambdaHandler():
    def __init__(self, event, context, logger) -> None:
        self.event = event
        self.context = context
        self.logger = logger
        self.location, self.max_radius, self.min_bdrooms, self.max_price = self.get_config()
    
    @staticmethod
    def get_config() -> (str, str, str, str):
        with open('src/resources/config.json', 'r') as f:
            config_data: dict = json.load(f)
    
        for key, val in config_data.items():
            if key != 'location':
                try:
                    _ = int(val)
                except ValueError:
                    sys.exit(f'Error: Your {key} must be an integer. Use "rental-alerts --config" to update.')
        
        location:     str = config_data['location']
        max_radius:   str = config_data['radius_miles']
        min_bedrooms: str = config_data['min_bedrooms']
        max_price:    str = config_data['max_price']

        return location, max_radius, min_bedrooms, max_price
    
    def get_new_listings(self) -> list | None:
        rm = Rightmove(self.logger, self.location, self.max_radius, self.min_bedrooms, self.max_price)
        rm_properties: list = rm.get_todays_listings()

        #zoopla = Zoopla(self.logger, self.location, self.max_radius, self.min_bedrooms, self.max_price)
        #zoopla_properties: list = zoopla.get_todays_listings()

        otm = OnTheMarket(self.logger, self.location, self.max_radius, self.min_bedrooms, self.max_price)
        otm_properties: list = otm.get_todays_listings()
        
        all_properties: list = rm_properties + otm_properties  # zoopla_properties + otm_properties
        return all_properties
    
    def update_cache(self, properties: list) -> None:
        with open('resources/todays_properties.json', 'r') as f:
            current_data = json.load(f)
            updated_data = current_data['publishedToday'] + properties
        with open('resources/todays_properties.json', 'w') as f:
            json.dump({"publishedToday": updated_data}, f)

    def clear_cache(self) -> None:
        with open('resources/todays_properties.json', 'w') as f:
            json.dump({"publishedToday": []}, f)

    def run(self) -> None:
        new_properties = self.get_new_listings()
        
        if not new_properties:
            self.logger.info('Nothng new found.')
            return

        format_listings = f'New listings as of {datetime.now().strftime("%H-%M-%s")}:\n'
        for prop in new_properties:
            format_listings += f'{prop["url"]}\n\n'

        #send_sms(format_listings)
        #self.logger.info(f'Atlassian server mail response: {str(send_email_atlassian_server(format_listings))}')
        self.logger.info(f'Response when sending e,ail with Python smtplib client: {send_email(format_listings)}')
        self.logger.info(f'Twilio SMS alert response: {send_sms(format_listings)}')

        current_hour = datetime.now().strftime('%H')
        if int(current_hour) >= 21:
            self.logger.info('Clearning today\'s history...')
            self.clear_cache()
            return
        
        self.update_cache(new_properties)



    
    
