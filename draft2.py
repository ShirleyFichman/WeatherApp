from flask import Flask, url_for, render_template
import requests
from pprint import pprint

# add try and except, meaningful naming, make everything more pythonic
#display - would like it to be presented in table like for each city- a column

def getMinDict():
    global lowest_temp_city  # saves the name of the city with the lowest temp_min
    lowest_temp_num = 1000 # entered an impossible value in order to init
    lst = ['Tel-aviv', 'Berlin', 'Budapest']
    d_min_values = {} #init result dict
    for city in lst:
        url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=4796f3765df8979006c4bc9c3ffc6719&units=metric'.format(
            city)
        res = requests.get(url)  # to get the data from the url
        data = res.json()  # to get the actual data in dict format
        temp_min = data['list'][0]['main']['temp_min'] #init temp_min
        curr_min_info = data['list'][0]['main'] #init curr_min_info
        for temperature_info in data['list'][1:]:
            curr_temp = temperature_info['main']['temp_min']
            if curr_temp < temp_min:
                curr_min_info = (temperature_info['main'])
                temp_min = curr_temp
        d1 = {city: curr_min_info}
        d_min_values.update(d1)
        if temp_min < lowest_temp_num:
            lowest_temp_city = city
            lowest_temp_num = temp_min
    #temp_min_list = [(k, d_min_values[k]['temp_min']) for k in d_min_values] -- Not sure if needed
    return d_min_values # return the dictionary of City:
                        # Weather data of the specific 3 hour frame which the temp_min is the lowest


app = Flask(__name__) #referncing this file
@app.route("/get_lowest_temp") #telling it where to go, like a domain, decorator
def get_lowest_temp(): #homepage
   return render_template("index.html", d_min_values=getMinDict(), lowest_temp_city=lowest_temp_city) #runs whatever is within index.html

if __name__== "__main__":
    app.run()




