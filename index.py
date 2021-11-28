#! ./venv1/Scripts/python

from flask import Flask, render_template, request, flash, redirect
import sys
import json
import requests
import pycountry
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
cards = {}


@app.route('/')
def index():
    return render_template('index.html', cards=cards.values())


@app.route('/add', methods=['POST'])
def add_city():

    def get_time_of_day(data):
        locale_time = time.gmtime(data['dt'] + data['timezone'])
        locale_hour = locale_time.tm_hour
        if locale_hour in range(0, 6):
            return 'night'
        if locale_hour in range(12, 18):
            return 'day'
        return 'evening-morning'

    def parse_weather(data):
        locale = data['sys']['country']
        country = pycountry.countries.get(alpha_2=locale).name
        # f = open("1.json", "w", encoding='utf-8')
        # f.write(json.dumps(data, ensure_ascii=False))
        return {
            'degrees': data['main']['temp'],
            'icon_code': data['weather'][0]['icon'],
            'city': data['name'],
            'state': data['weather'][0]['description'],
            'country': country,
            'time_of_day': get_time_of_day(data)
        }

    city = request.form['city_name']
    params = {
        'q': city,
        'appid': 'ec9ff91f78b1727c305789d61166a28b',
        'lang': 'ru',
        'units': 'metric'
    }
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather', params=params)
    if response:
        weather_data = parse_weather(response.json())
        city_name = weather_data['city']
        cards[city_name] = weather_data
        return render_template('index.html', cards=cards.values())
    flash('Город не найден')
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete_city():
    print(request.form['id'])
    city_name = request.form['id']
    del cards[city_name]
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
