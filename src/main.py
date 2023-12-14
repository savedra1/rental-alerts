import sys
import os
import json

from scrapers.rightmove import Rightmove

def main():
    with open('src/resources/config.json', 'r') as f:
        config_data: dict = json.load(f)
    
    location:     str = config_data['location']
    max_radius:   str = config_data['radius_miles']
    min_bedrooms: str = config_data['min_bedrooms']
    max_price:    str = config_data['max_price']


    rm = Rightmove(location, max_radius, min_bedrooms, max_price)
    rm_properties: list | None = rm.get_todays_properties()

    print(rm_properties)


if __name__ == "__main__":
    main()