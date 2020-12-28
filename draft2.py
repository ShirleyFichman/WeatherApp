from flask import Flask, url_for, render_template
import requests
from pprint import pprint


# add try and except, make everything more pythonic
# display - would like it to be presented in table like for each city- a column

def getMinDict():
    global lowest_temp_city  # saves the name of the city with the lowest temp_min
    lowest_temp_num = None  # will save the lowest temperature overall, for lowest_temp_city
    city_lst = ['Tel-aviv', 'Berlin', 'Budapest']
    d_min_values = {}  # init the result dictionary
    for city in city_lst:
        url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=4796f3765df8979006c4bc9c3ffc6719&units=metric'.format(
            city)
        res = requests.get(url)  # get data from the url
        data = res.json()  # to get the data in a dict format
        curr_temp_min = data['list'][0]['main']['temp_min']  # init
        curr_info_min = data['list'][0]['main']  # init
        for temperature_info in data['list'][1:]:  # iterate on the every 'main' to find lowest temp_min
            curr_temp = temperature_info['main']['temp_min']
            if curr_temp < curr_temp_min:  # update curr_temp_min and save the min_info for the future res dict
                curr_info_min = (temperature_info['main'])
                curr_temp_min = curr_temp
        d_curr = {city: curr_info_min}  # saves the city with the info that's with the lowest temp_min
        d_min_values.update(d_curr)  # update our result dict with the new city and data
        if lowest_temp_num == None:  # init, for the first iteration
            lowest_temp_city = city
            lowest_temp_num = curr_temp_min
        elif curr_temp_min < lowest_temp_num:  # checks for the lowest temp_min overall, comparing cities
            lowest_temp_city = city
            lowest_temp_num = curr_temp_min
    return d_min_values
    # return the dictionary of (City: Weather Data) of the specific 3 hour frame which temp_min is the lowest


app = Flask(__name__)  # reference this file


@app.route("/get_lowest_temp")
def get_lowest_temp():
    return render_template("index.html", d_min_values=getMinDict(),
                           lowest_temp_city=lowest_temp_city)  # runs whatever is within index.html


if __name__ == "__main__":
    app.run()


