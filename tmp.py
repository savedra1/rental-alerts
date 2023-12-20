
import cloudscraper
import requests
import json



"""scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
print(scraper.get("https://www.zoopla.co.uk/to-rent/houses/london/?beds_max=2&price_frequency=per_month&price_max=600&property_sub_type=detached&property_sub_type=semi_detached&property_sub_type=terraced&q=London&radius=3&results_sort=newest_listings&search=to-rent"
).status_code) """

"""headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}"""

"""response = requests.get('https://www.zoopla.co.uk/to-rent/houses/london/?beds_max=2&price_frequency=per_month&price_max=600&property_sub_type=detached&property_sub_type=semi_detached&property_sub_type=terraced&q=London&radius=3&results_sort=newest_listings&search_source=to-rent',
                        headers = headers)"""


"""def make_req(cookies=None):
    url = "https://www.zoopla.co.uk/to-rent/houses/london/?beds_max=2&price_frequency=per_month&price_max=600&property_sub_type=detached&property_sub_type=semi_detached&property_sub_type=terraced&q=London&radius=3&results_sort=newest_listings&search_source=to-rent"

    # Payload parameters
    payload = {
        'beds_max': 2,
        'price_frequency': 'per_month',
        'price_max': 600,
        'property_sub_type': ['detached', 'semi_detached', 'terraced'],
        'q': 'London',
        'radius': 3,
        'results_sort': 'newest_listings',
        'search_source': 'to-rent'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': 'https://www.google.com/',
        'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
    }
    if cookies:
        response = requests.get(url, params=payload, headers=headers, cookies=cookies)
    else:
        response = requests.get(url, params=payload, headers=headers)
    # Print the status code and content
    #print("Status Code:", response.status_code)
    #print("Response Content:", response.text)

    print(response.cookies)

cookies = make_req()
#make_req(cookies)

print('Updated4')"""


url = "https://www.zoopla.co.uk/to-rent/houses/london/?beds_max=2&price_frequency=per_month&price_max=600&property_sub_type=detached&property_sub_type=semi_detached&property_sub_type=terraced&q=London&radius=3&results_sort=newest_listings&search=to-rent"



apikey = '425c7f0e256f581278ea86502ac1045e62b92e56'
params = {
    'url': url,
    'apikey': apikey,
	'js_render': 'true',
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
print(response.text)