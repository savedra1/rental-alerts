
import json
from datetime import datetime

import re

from utils.constants import ZOOPLA_HTML_EXTRACTION
from utils.convert_date import zoopla_date_convert
from utils.json_cleaner import clean_json

#from playwright.sync_api import sync_playwright
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options


class Zoopla:
    def __init__(self, logger, location, max_radius, min_bedrooms, max_price):# -> None:
        self.logger = logger
        self.location = location
        self.max_radius = max_radius
        self.min_bedrooms = min_bedrooms
        self.max_price = max_price
        self.base_url = 'https://www.zoopla.co.uk/to-rent/property/'
        self.agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        

    def construct_url(self) -> str:
        return f'\
            https://www.zoopla.co.uk/to-rent/property/\
            {self.min_bedrooms}-bedrooms/{self.location}/?\
            price_frequency=per_month\
            &price_max={self.max_price}\
            &q=Bristol%20City%20Centre%2C%20Bristol\
            &radius={self.max_radius}\
            &results_sort=newest_listings&search_source=to-rent'.replace(' ', '')

    def extract_data(self, html_data):# -> list | None:
        try:
            properties_data_str = clean_json(
                html_data.split(ZOOPLA_HTML_EXTRACTION['start'])[1].split(ZOOPLA_HTML_EXTRACTION['end'])[0]
            )
            return json.loads('{"properties":'+properties_data_str+'}')['properties']
        except Exception:
            self.logger.error('Error: Unable to extract valid JSON from Zoopla\'s HTML response. extraction points may need updating.')
            return None

        # RegEx seems to have a problem parsing the html from Zoopla - To be looked into                          
        """data_pattern = re.compile(
            re.escape(ZOOPLA_HTML_EXTRACTION['start']) + r'({.*?})' + re.escape(ZOOPLA_HTML_EXTRACTION['end'])    
        )
        match = data_pattern.search(clean_json(html_data))                                                              
        if match:
            try:
                properties: list = json.loads(
                    clean_json('{"properties":' + match.group(1) + '}')
                )['properties']
                return properties
            except json.JSONDecodeError:
                self.logger.error('Error: Unable to extract valid JSON from Zoopla\'s HTML response.')
                return None
            
        self.logger.error('Zoopla web response has been updated. Unable to parse result.')
        return None"""

    def get_html_response(self):# -> str | None:
        query_url = self.construct_url()
        self.loger.info('Loading selenium webdriver...')
        try:
            options = Options()
            options.binary_location = '/opt/headless-chromium'
            options.add_argument('--headless')  # Run Chrome in headless mode
            options.add_argument('--no-sandbox')
            options.add_argument('--single-process')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')

            driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
            driver.get(query_url)
            html_content = driver.page_source
            return html_content
        
        except Exception as err:
            self.logger.error(f'Selenium webdriver failed to return a valid HTML response from Zoopla:\n{err}')
            return None

    def get_todays_listings(self):# -> list | None:
        html_response: str | None = self.get_html_response()
        if not html_response:
            return None
        
        properties_data: list | None = self.extract_data(html_response)
        if not properties_data:
            return None
        
        self.logger.info(f'Zoopla properties found: {str(properties_data)}')
        today = datetime.now().strftime('20%y-%m-%d')
        todays_publications = []

        for num, property in enumerate(properties_data, start=1):
            self.logger.info(f'{str(num)} | Property: {property["listingId"]} | Published: {property["lastPublishedDate"]}')
            published_val_reformatted: str | None = zoopla_date_convert(property['publishedOn'])

            if published_val_reformatted == today: #\ 'lastPublishDate' includes any updates so omitting this logic to ensure only new listings are added.
            #or published_val_reformatted == today: property['lastPublishedDate'].split('T')[0] == today
                todays_publications.append({
                    'id': property['listingId'],
                    'url': f'https://zoopla.co.uk{property["listingUris"]["detail"]}',
                    'price': property['price'],
                    'listed_date': property['publishedOn']
                })

        return todays_publications

        
        
