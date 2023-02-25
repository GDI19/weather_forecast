from datetime import datetime

import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CityForm


def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        try:
            form.is_valid()
            context = get_data(form.cleaned_data['name'])
            return render(request, 'weather_forecast/index.html', context)
        except:
            messages.error(request, 'City name is not correct. Please try to enter correct name.')
            return redirect(index)

    #city = 'Moscow'
    #context = get_data(city)
    form = CityForm()
    context = {'form': form}
    return render(request, 'weather_forecast/index.html', context)


def get_data(city):
    days_index_list = [0, 8, 16, 24, 32, 39]
    weather_5days_list = []
    url_geo = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid=6f9b5463e6469f3078746f08677709b4'
    coordinates_from_api = requests.get(url_geo.format(city)).json()
    print(coordinates_from_api)
    latitude = round(coordinates_from_api[0]['lat'], 2)
    longitude = round(coordinates_from_api[0]['lon'], 2)
    #print(type(latitude), longitude)

    url_5days = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=6f9b5463e6469f3078746f08677709b4&units=metric'
    data_from_api = requests.get(url_5days.format(lat=latitude, lon=longitude)).json()
    #print(data_from_api)

    timezone_sec = int(data_from_api['city']['timezone'])
    timezone = timezone_sec / 3600
    sunrise = datetime.utcfromtimestamp((data_from_api['city']['sunrise'] + timezone_sec))
    sunset = datetime.utcfromtimestamp((data_from_api['city']['sunset'] + timezone_sec))

    city_info = {
        'name': city,
        'country': data_from_api['city']['country'],
        # 'population': data_from_api['city']['population'],
        'timezone': timezone,
        'sunrise': sunrise,
        'sunset': sunset,
    }

    for d in days_index_list:
        item = data_from_api['list'][d]
        weather_dict = {
                'day': item['dt_txt'],
                'temperature' : item['main']['temp'],
                'humidity' : item['main']['humidity'],
                'description' : item['weather'][0]['description'],
                'icon' : item['weather'][0]['icon'],
                'wind_speed' : item['wind']['speed'],
                'wind_gust' : item['wind']['gust'],
            }
        weather_5days_list.append(weather_dict)

    form = CityForm()
    context = {'weather': weather_5days_list, 'city_info': city_info, 'form': form}
    return context
