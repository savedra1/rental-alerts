"""
Main lambda function code for project |
_____________________________________ |
                                      |
Author: Michael S                     |
Date: 2023-12-15                      |
"""

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
from utils.email_client import send_email 
from utils.aws_utils import AWSUtils

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
        logger.info(f'Response when sending error alert to admin: {alert_admin(err_msg)}')
        function_response['statusCode'] = 500
        function_response['body'] = str(err_msg)


class LambdaHandler():
    def __init__(self, event, context, logger) -> None:
        self.event = event
        self.context = context
        self.logger = logger
        self.location, self.max_radius, self.min_bedrooms, self.max_price = self.get_config()
        self.awsu = AWSUtils()
    
    @staticmethod
    def get_config() -> (str, str, str, str):
        with open('resources/config.json', 'r') as f:
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
    
    def update_cache(self, properties: list) -> bool:
        try:
            current_data: str = self.awsu.get_parameter('/rental_alerts/daily_cache')
            updated_data = current_data + str(properties)
            self.awsu.update_parameter('/rental_alerts/daily_cache', str(updated_data))
            return True
        except Exception as err:
            self.logger.error(err)
            return False

    def clear_cache(self) -> bool:
        try:
            self.awsu.update_parameter('/rental_alerts/daily_cache', '[]')
            return True
        except Exception as err:
            self.logger.error(err)
            return False
        
    def run(self) -> None:
        todays_listings_cache: str = self.awsu.get_parameter('/rental_alerts/daily_cache')
        self.logger.info(f'Currently in cache: {todays_listings_cache}')
        properties: list = self.get_new_listings()

        new_properties = [prop for prop in properties if prop['id'] not in todays_listings_cache]
        
        if not new_properties:
            self.logger.info('Nothng new found.')
            return
        
        format_listings = f'New listings as of {datetime.now()}:\n\n'
        for prop in new_properties:
            format_listings += f'{prop["url"]}\n\n'
        
        self.logger.info(format_listings)

        self.logger.info(f'Response when sending email with Python smtplib client: {send_email(format_listings)}')
        self.logger.info(f'Twilio SMS alert response: {send_sms(format_listings)}')

        current_hour: str = datetime.now().strftime('%H')
        if int(current_hour) >= 21:
            self.logger.info('Clearning today\'s history...')
            self.clear_cache()
            return
        
        cache_updated = self.update_cache([prop['id'] for prop in new_properties])
        if cache_updated:
            self.logger.info('Execution completed successfully.')
        else:
            self.logger.error('Execution completed but failed to update property cache.')

    
    
