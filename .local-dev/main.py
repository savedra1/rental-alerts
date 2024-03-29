# !main

import sys
import json

from scrapers.rightmove import Rightmove
from scrapers.zoopla import Zoopla
from scrapers.on_the_market import OnTheMarket

from utils.logger import set_up_logger

def main():
    logger = set_up_logger()
    
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

    rm = Rightmove(logger, location, max_radius, min_bedrooms, max_price)
    rm_properties: list | None = rm.get_todays_listings()

    zoopla = Zoopla(logger, location, max_radius, min_bedrooms, max_price)
    zoopla_properties: list | None = zoopla.get_todays_listings()

    otm = OnTheMarket(logger, location, max_radius, min_bedrooms, max_price)
    otm_properties: list | None = otm.get_todays_listings()
    
    all_properties: list = rm_properties + zoopla_properties + otm_properties
    if not all_properties:
        logger.info('Nothng new found.')
        return

    with open('src/resources/todays_properties.json', 'r') as f:
        todays_data: dict = json.load(f)
        all_properties: list = [
            property for property in all_properties if property not in todays_data['publishedToday']
        ]
    
    logger.info('PROPERTY DATA:\n\n')
    for property in all_properties:
        logger.info(
              f'*** New listings found ***\n| Property id: {property["id"]}\n| Price: {property["price"]}\n| Link: {property["url"]}\n| Listed: {property["listed_date"]}\n___________________________\n\n'
        )

if __name__ == "__main__":
    main()
