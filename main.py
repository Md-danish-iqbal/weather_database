import pymongo

from input import indian_cities, base_url, key, air_quality_data
import requests
import logging
import configparser
from pymongo import MongoClient
import pandas as pd
import json


def weather_data_generator():
    try:
        data_list = []
        for metro_cities in indian_cities:
            url = base_url + key + ' &q=' + metro_cities + '&aqi' + air_quality_data
            r = requests.get(url, timeout=3)
            r.raise_for_status()
            data = json.loads(r.text)

            location = data['location']['name']
            region = data['location']['region']
            local_time = data['location']['localtime']
            current_temp_in_celsius = data['current']['temp_c']
            current_temp_in_fahrenheit = data['current']['temp_f']
            feels_like = data['current']['condition']['text']

            # print(location, region, local_time, current_temp_in_celsius, current_temp_in_fahrenheit, feels_like)

            temp = {'Location': location, 'Region': region, 'Time': local_time,
                    'Temperature_Degree_Celsius': current_temp_in_celsius,
                    'Temperature_Degree_Fahrenheit': current_temp_in_fahrenheit,
                    'Weather_feels_like': feels_like}
            data_list.append(temp)

        return data_list
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)


if __name__ == "__main__":
    list_of_values = weather_data_generator()
    print("hello mongo db")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['weather_data']
    collection = db['sample_collection']
    collection.insert_many(list_of_values)

