import requests
import json
from datetime import datetime, timedelta

import cloudscraper

import re

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup



#TODO:
"""
- Convert dates for date check
- Build master class
- Build cloudwatch trigger
- Build lambda function
- Decide on best method for emailing / watspapping results
"""

def convert_date_format(date_str):
    # Convert month to its corresponding number
    date_str = date_str.replace(' ', '')
    year = '23'
    try:
        day = str(int(date_str[0:2]))
        double_digit_day = True
    except ValueError:
        day = str(int(date_str[0:1]))
        double_digit_day = False
    
    if double_digit_day:
        alpha_month = date_str[4:7]
    else:
        alpha_month = date_str[3:6]
        day = '0' + day
    
    month_dict = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    numeric_month = month_dict[alpha_month]

    return f'{str(day)}/{numeric_month}/{year}'
    

def right_move(today, yesterday):
    bristol: str = '%5E219'
    min_beds: str = '2'
    max_price: str = '1300' 
    miles_from_center: str = '5'
    #url = """https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E219&insId=1&radius=3.0&minPrice=&maxPrice=1300&minBedrooms=&maxBedrooms=2&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare="""
    agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    url = f'\
    https://www.rightmove.co.uk/property-to-rent/find.html?\
    locationIdentifier=REGION{bristol}\
    &minBedrooms={min_beds}\
    &maxPrice={max_price}\
    &radius={miles_from_center}\
    &propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=\
    '.replace(' ', '')

    response = requests.get(url, headers={'User-Agent': agent})

    properties: list = json.loads(
        response.text.split(
            '<script>window.jsonModel = ')[1].split(
                '</script><script>'
            )[0]
        )['properties']

    for num, property in enumerate(properties, start=1):
        #print(property)
        added_date: str = property['addedOrReduced']
        print(added_date)
        property_url = property['propertyUrl']
        property_price = property['price']['amount']

        if added_date == today or added_date == yesterday:
            print(
                f'{num}:\n£{property_price}\
                \nhttps://rightmove.co.uk{property_url}\
                \n{added_date}'\
                '\n\n'
            )


def clean_json(json_string):
    bad_strings = [
        '"])</script><script>self.__next_f.push([1,"',
        '1,\n',
        ']")</script><script>self.__next_f.push("['
    ]
    for string in bad_strings:
        json_string = json_string.replace(string, '')
    return json_string


def zoopla(today, yesterday):
    min_beds: str = '2'
    max_price: str = '1300' 
    miles_from_center: str = '3'
    url = f'\
        https://www.zoopla.co.uk/to-rent/property/\
        {min_beds}-bedrooms/bristol-city-centre/?\
        price_frequency=per_month\
        &price_max={max_price}\
        &q=Bristol%20City%20Centre%2C%20Bristol\
        &radius={miles_from_center}\
        &results_sort=newest_listings&search_source=to-rent'.replace(' ', '')
    
    agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent=agent)
        page = context.new_page()

        # Navigate to the URL
        page.goto(url)
        # Wait for the page to load
        page.wait_for_load_state("load")
        # Get the page source using Playwright
        page_src = page.content()
        clean_src = str(page_src).replace('\\', '')
        properties_data_str = clean_json('{"properties":' + clean_src.split(
            '"regularListingsFormatted":')[1].split(
                ',"mobile"')[0].split(
                    ',"transactionType"')[0] + '}'
        )

        properties_data: list = json.loads(properties_data_str)['properties']
        

        #print(properties_data)
        

    for num, property in enumerate(properties_data, start=1):
        if convert_date_format(property["publishedOn"]) == today \
        or convert_date_format(property["publishedOn"]) == yesterday:
            print(f'\
                {num}:\
                \nhttps://zoopla.co.uk{property["listingUris"]["detail"]}\
                \n{property["price"]}\
                \n{convert_date_format(property["publishedOn"])}\
                \n\n'.replace(' ', '')
            )


def on_the_market():
    url = 'https://www.onthemarket.com/to-rent/2-bed-property/bristol/?max-price=1500&radius=0.5'
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    properties: list = json.loads(response.text.split(
        ' __OTM__.globals = ')[0].split(
            '__OTM__.jsonData = ')[1][:-3])['properties']
    
    for num, property in enumerate(properties, start=1):
        if not property.get('ad?'):
            print(f'\
                {num}:\
                \nhttps://onthemarket.com{property["property-link"]}\
                \n{property["price"]}\
                \n{property["days-since-added-reduced"]}\
                \n\n'.replace(' ', '')
            )


class RightMove:
    def __init__(self) -> None:
        self.bristol: str = '%5E93829'
        self.min_beds: str = '2'
        self.max_price: str = '1300' 
        self.miles_from_center: str = '3'
        self.url = f'\
        https://www.rightmove.co.uk/property-to-rent/find.html?\
        locationIdentifier=REGION{self.bristol}\
        &minBedrooms={self.min_beds}\
        &maxPrice={self.max_price}\
        &radius={self.miles_from_center}\
        &propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=\
        '
        self.all_properties = self.get_all_properties()
    
    def get_all_properties(self) -> list:
        response = requests.get(self.url)

        properties: list = json.loads(
            response.text.split(
                '<script>window.jsonModel = ')[1].split(
                    '</script><script>'
                )[0]
            )['properties']
        
        return properties
    
    def get_new_properties(self) -> list:
        new_properties = []
        for num, property in enumerate(self.properties):
            added_date: str = property['addedOrReduced']
            property_url = property['propertyUrl']
            property_price = property['price']['amount']

        if added_date == 'TODAY':
            new_properties.append(
                {
                    'price': f'£{property_price}',
                    'url': f'https://rightmove.co.uk/{property_url}',
                    'added_date': added_date
                }
            )
        return new_properties

if __name__ == "__main__":
    today = datetime.now().strftime('%d/%m/%y')
    yesterday_delta = datetime.now() - timedelta(days=1)
    yesterday = yesterday_delta.strftime('%d/%m/%y')

    #zoopla(today, yesterday)
    right_move(today, yesterday)
