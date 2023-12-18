

import json

from utils.web_session import get_requests_session
from utils.constants import OTM_HTML_EXTRACTION


class OnTheMarket():
    def __init__(self, logger, location, max_radius, min_bedrooms, max_price):# -> None:
        self.logger = logger
        self.location = location
        self.max_radius = max_radius
        self.min_bedrooms = min_bedrooms
        self.max_price = max_price
        self.base_url = 'https://www.onthemarket.com/to-rent/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        }
    
    def construct_url(self):# -> str:
        return f'{self.base_url}{self.min_bedrooms}-bed-property/{self.location}/?max-price={self.max_price}&radius={self.max_radius}'

    def extract_data(self, html_string: str) -> list | None:
        try:
            properties: list = json.loads(html_string.split(
                OTM_HTML_EXTRACTION['end'])[0].split(
                OTM_HTML_EXTRACTION['start'])[1][:-3]
            )['properties']        

            return properties
        
        except Exception as err:
            self.logger.error(f'Failed to extract property list from OTM\' HTML response:\n{err}' )
            return None

    def get_todays_listings(self):
        query_url = self.construct_url()
        
        with get_requests_session() as web_session:
            response = web_session.get(query_url, headers=self.headers)
        
        property_data: list | None = self.extract_data(response.text)

        if not property_data:
            return None
        
        self.logger.info(f'Rightmove properties found: {str(property_data)}')

        todays_listings = []
        for num, property in enumerate(property_data, start=1):
            if property.get('ad?'):
                continue 

            self.logger.info(f'{str(num)} | Property: {property["id"]} | Published: {property["days-since-added-reduced"]}')

            if property['days-since-added-reduced'].split(' ')[1] == 'today':
                todays_listings.append({
                    'id': property['id'],
                    'url': f'https://onthemarket.com{property["property-link"]}',
                    'price': property['price'],
                    'listed_date': property['days-since-added-reduced'].split(' ')[1]
                })
        
        return todays_listings
                
