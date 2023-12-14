import requests
import json
import sys
from datetime import datetime


class Rightmove():
    def __init__(self, location, max_radius, min_bedroom, max_price) -> None:
        self.region_id: str = self.get_region_code(location) 
        self.max_radius: str = self.verify_integer('radius', max_radius)
        self.min_bedrooms: str = self.verify_integer('max_bedrooms', min_bedroom)
        self.max_price: str = self.verify_integer('max_price', max_price)
        self.base_url = 'https://www.rightmove.co.uk/property-to-rent/find.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        }
    
    @staticmethod
    def get_region_code(location: str) -> str:
        with open ('src/resources/rightmove_location_codes.json', 'r') as f:
            json_data = json.load(f)
        
        region_id = json_data.get(location.lower(), None)

        if not region_id:
            sys.exit(f'Could not find a region ID for {location}.')
        return region_id
       
    @staticmethod
    def verify_integer(param_name, value: str) -> str:
        try:
            _ = int(value)
            return value
        except Exception:
            sys.exit(f'Error: Rightmove {param_name} must be an integer.')
    
    def construct_url(self):
        return f'\
            {self.base_url}?\
            locationIdentifier=REGION{self.region_id}\
            &minBedrooms={self.min_bedrooms}\
            &maxPrice={self.max_price}\
            &radius={self.max_radius}\
            &includeLetAgreed=false\
            &includeLetAgreed=false'.replace(' ', '')

    def extract_data(self, html_string: str) -> list:
        try:
            properties = json.loads(
                html_string.split(
                    '<script>window.jsonModel = ')[1].split(
                        '</script><script>'
                    )[0]
                )['properties']
        except Exception:
            print('Failed to parse rightmove HTML response.')
            return None
        
        if not type(properties) is list and not type(properties) is None:
            print(f'Failed to extract properties list form html response: {self.construct_url()}')
            return None
        return properties
    
    def get_todays_properties(self) -> list | None:
        query_url = self.construct_url()

        response = requests.get(query_url, headers=self.headers)
        properties: list = self.extract_data(response.text)
        
        if not properties:
            return None
        
        todays_properties = []
        for num, property in enumerate(properties, start=1):
            if property['addedOrReduced'].lower() == 'added today'\
            or property['firstVisibleDate'].split('T')[0] == datetime.now().strftime('%y-%m-%d'):
                todays_properties.append({
                    'index': str(num),
                    'property_url': f'https://rightmove.co.uk{property["propertyUrl"]}',
                    'property_price': property['price']['amount']
                })

        return todays_properties

        






        



    




