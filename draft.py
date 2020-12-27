from flask import Flask, url_for, render_template
import requests
from pprint import pprint

# this is the part that is relevant to the open weather API
lst = ['Tel-aviv', 'Berlin', 'Budapest']
for city in lst:
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=4796f3765df8979006c4bc9c3ffc6719&units=metric'.format(
        city)
    res = requests.get(url)  # to get the data from the url
    data = res.json()  # to get the actual data in dict format
    temp_min = data['list'][0]['main']['temp_min']
    for x in range(1, 40):  # 39 is the last one! 40 iterations for each 3 hours- goes through 5 days
        y = data['list'][x]['main']['temp_min']
        if y < temp_min:
            temp_min = y
    print('city: ', city)
    print('temp_min: ', temp_min)
#

app = Flask(__name__) #referncing this file
@app.route("/") #telling it where to go, like a domain
def home(): #homepage
   return render_template("index.html", content=lst, temp=temp_min) #runs whatever is within index.html

if __name__== "__main__":
    app.run()
