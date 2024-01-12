import json
import re
from datetime import datetime

from utils.constants import RIGHTMOVE_HTML_EXTRACTION
from utils.web_session import get_requests_session

class Rightmove():
    def __init__(self, logger, location, max_radius, min_bedroom, max_price):# -> None:
        self.logger = logger
        self.region_id: str = self.get_region_code(location) 
        self.max_radius: str = max_radius
        self.min_bedrooms: str = min_bedroom
        self.max_price: str = max_price
        self.base_url = 'https://www.rightmove.co.uk/property-to-rent/find.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        }
    
    @staticmethod
    def get_region_code(location: str):# -> str:
        with open ('resources/rightmove_location_codes.json', 'r') as f:
            json_data = json.load(f)
        
        return json_data.get(location.lower(), None)

    def construct_url(self):
        return f'\
            {self.base_url}?\
            locationIdentifier=REGION{self.region_id}\
            &minBedrooms={self.min_bedrooms}\
            &maxPrice={self.max_price}\
            &radius={self.max_radius}\
            &includeLetAgreed=false\
            &includeLetAgreed=false'.replace(' ', '')

    def extract_data(self, html_string: str):# -> list:
        data_pattern = re.compile(
            re.escape(RIGHTMOVE_HTML_EXTRACTION['start']) + r'({.*?})' + re.escape(RIGHTMOVE_HTML_EXTRACTION['end'])
        ) 
        match = data_pattern.search(html_string)
        if match:
            return json.loads(match.group(1))['properties']
        
        self.logger.error(f'Rightmove HTML response has been updated:\n{str(html_string)}')
        return None
    
    def get_todays_listings(self):# -> list | None:
        if not self.region_id:
            self.logger.warn(f'Could not find a region ID for {self.location}. Find instructions on how to add your region ID here:')
            return None

        query_url = self.construct_url()

        with get_requests_session() as web_session:
            response = web_session.get(query_url, headers=self.headers)

        properties: list = self.extract_data(response.text)
        
        if not properties:
            return None
        
        self.logger.info(f'Rightmove properties found: {str(properties)}')
        today = datetime.now().strftime('20%y-%m-%d')
        todays_properties = []
        for num, property in enumerate(properties, start=1):
            self.logger.info(f'{str(num)} | Property: {property["id"]} | Published: {property["addedOrReduced"]}')
            if property['addedOrReduced'].lower() == 'added today'\
            or property['firstVisibleDate'].split('T')[0] == today: 
                todays_properties.append({
                    'id': str(property['id']),
                    'url': f'https://rightmove.co.uk{property["propertyUrl"]}',
                    'price': property['price']['amount'],
                    'listed_date': property['addedOrReduced']
                })

        return todays_properties
