from input import indian_cities, base_url, key, air_quality_data
import requests

try:
    for metro_cities in indian_cities:
        url = base_url + key + ' &q=' + metro_cities + '&aqi' + air_quality_data
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        print(r.text)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)
except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)

    # OOps: Something Else 404 Client Error: Not Found for url: http://www.google.com/blahblah
