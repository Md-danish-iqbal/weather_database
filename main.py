import pymongo

from input import indian_cities, base_url, key, air_quality_data
import requests
import logging
import json
import configparser
from pymongo import MongoClient
import pandas as pd


logging.basicConfig(filename='./logs/logs.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


def weather_data_generator():
    data_list = []
    for metro_cities in indian_cities:
        try:
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

            logging.info(f'Data collected successfully for {location}')

            temp = {'Location': location, 'Region': region, 'Time': local_time,
                    'Temperature_Degree_Celsius': current_temp_in_celsius,
                    'Temperature_Degree_Fahrenheit': current_temp_in_fahrenheit,
                    'Weather_feels_like': feels_like}
            data_list.append(temp)
            logging.info(f'Data appended into the list successfully for {location}')

        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logging.error("OOps: Something Else", err)
        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error:", errh)

    return data_list


if __name__ == "__main__":
    list_of_values = weather_data_generator()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    logging.info('connected to MongoClient successfully')
    db = client['weather_data']
    collection = db['sample_collection']
    collection.insert_many(list_of_values)
    logging.info('data added successfully to the mongo database')
