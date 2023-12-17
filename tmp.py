import requests
url = "https://www.zoopla.co.uk/to-rent/property/bristol/?beds_min=2&price_frequency=per_month&price_max=1500&q=Bristol&radius=3&results_sort=newest_listings&search_source=to-rent"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'}

response = requests.get(url, headers=headers)
print(response.text)