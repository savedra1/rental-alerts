import json

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

import logging
import sys
import traceback

def lambda_handler(event, context):
    function_response = {
        'statusCode': 200,
        'body': {
            'response_data': None
        }
    }
    print(event)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    query_url = event['body']['url']
    logger.info(f'Query URL: {query_url}')

    logger.info('Loading selenium webdriver...')
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

        function_response['body'] = json.dumps({
            'response_data': str(html_content)
        })
        return html_content

    except Exception as err:
        logger.error(f'Selenium webdriver failed to return a valid HTML response from Zoopla:\n{err}')
        function_response['statusCode'] = 500
        function_response['body'] = {
            'response_data': f'Failed to return a valid HTML respinse. Error message: {err}'
        }
        return function_response
