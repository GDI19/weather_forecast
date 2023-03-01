import time
from datetime import datetime

import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CityForm
from config import OPEN_WEATHER_API_KEY


def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        try:
            form.is_valid()
            city = form.cleaned_data['name']
            data_from_api = get_data(city)
            city_info = fill_city_info(data_from_api, city)
            five_days_forecast = fill_weather_forecast(data_from_api)
            form = CityForm()
            context = {'weather': five_days_forecast, 'city_info': city_info, 'form': form}
            return render(request, 'weather_forecast/index.html', context)
        except:
            messages.error(request, "City name is not correct. Please try to enter correct name.")

    form = CityForm()
    context = {'form': form}
    return render(request, 'weather_forecast/index.html', context)


def get_data(city):
    url_geo = 'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={key}'
    coordinates_from_api = requests.get(url_geo.format(city=city, key=OPEN_WEATHER_API_KEY)).json()
    latitude = round(coordinates_from_api[0]['lat'], 2)
    longitude = round(coordinates_from_api[0]['lon'], 2)

    url_5days = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}&units=metric'
    data_from_api = requests.get(url_5days.format(lat=latitude, lon=longitude, key=OPEN_WEATHER_API_KEY)).json()

    return data_from_api


def fill_city_info(data_from_api, city):
    timezone_sec = int(data_from_api['city']['timezone'])
    timezone = timezone_sec / 3600
    sunrise_local = datetime.utcfromtimestamp((data_from_api['city']['sunrise'] + timezone_sec)).strftime("  %d %b. %Y, %H:%M")
    sunset_local = datetime.utcfromtimestamp((data_from_api['city']['sunset'] + timezone_sec)).strftime("  %d %b. %Y, %H:%M")

    url_for_country = 'https://restcountries.com/v3.1/alpha/{}'
    country_code = data_from_api['city']['country']
    data_for_country = requests.get(url_for_country.format(country_code)).json()
    country_name = data_for_country[0]['name']['common']

    city_info = {
        'name': city,
        'country_name': country_name,
        'country_code': country_code,
        'timezone': timezone,
        'sunrise': sunrise_local,
        'sunset': sunset_local,
    }
    return city_info


def fill_weather_forecast(data_from_api):
    days_index_list = [0, 8, 16, 24, 32, 39]
    weather_5days_list = []

    for d in days_index_list:
        item = data_from_api['list'][d]
        datetime_object = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
        day = datetime_object.strftime('%a, %d %b. %Y')
        # print(day)
        weather_dict = {
                'day': day,
                'temperature' : item['main']['temp'],
                'humidity' : item['main']['humidity'],
                'description' : item['weather'][0]['description'],
                'icon' : item['weather'][0]['icon'],
                'wind_speed' : round(item['wind']['speed']),
                'wind_gust' : round(item['wind']['gust']),
            }
        weather_5days_list.append(weather_dict)

    return weather_5days_list
