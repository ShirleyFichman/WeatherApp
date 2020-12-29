from typing import Dict
from typing import List
from flask import Flask, url_for, render_template
import requests
from pprint import pprint

LIST = 'list'
MAIN = 'main'
TEMP_MIN = 'temp_min'
CITY = 'city'
URL = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=4796f3765df8979006c4bc9c3ffc6719&units=metric'

lowest_temp_city = None


def get_min_dict() -> Dict:
    cities_list = ['Tel-aviv', 'Berlin', 'Budapest']
    return create_dict(cities_list)


def create_dict(cities_list: List) -> Dict:
    min_data_dict = {}
    lowest_temp_overall = None
    for city in cities_list:
        city_data = get_data(city)
        curr_info_min = city_data[LIST][0][MAIN]
        curr_temp_min = curr_info_min[TEMP_MIN]
        min_data_dict = update_dict(city_data, curr_temp_min, city, min_data_dict, curr_info_min)
        if new_lowest_temp_overall(lowest_temp_overall, city, curr_temp_min):
            update_lowest_temp_city(city)
            lowest_temp_overall = curr_temp_min
    return min_data_dict


def update_lowest_temp_city(city):
    global lowest_temp_city
    lowest_temp_city = city


def get_data(city):
    curr_url = URL.format(city)
    response = requests.get(curr_url)
    return response.json()


def update_dict(city_data, curr_temp_min, city, min_data_dict, curr_info_min) -> Dict:
    for weather_info in city_data[LIST][1:]:
        curr_temp = weather_info[MAIN][TEMP_MIN]
        if curr_temp < curr_temp_min:
            curr_temp_min = curr_temp
            curr_info_min = (weather_info[MAIN])
    return add_city_to_dict(city, min_data_dict, curr_info_min)


def add_city_to_dict(city, min_data_dict, curr_info_min) -> Dict:
    dict_addition = {CITY: city}
    dict_addition.update(curr_info_min)
    min_data_dict[city] = dict_addition
    return min_data_dict


def new_lowest_temp_overall(lowest_temp_overall, city, curr_temp_min):
    if lowest_temp_overall is None:
        return True
    return curr_temp_min < lowest_temp_overall


app = Flask(__name__)


@app.route("/get_lowest_temp")
def get_lowest_temp():
    return render_template("index.html", min_data_dict=get_min_dict(),
                           lowest_temp_city=lowest_temp_city)


if __name__ == "__main__":
    app.run()
