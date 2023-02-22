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

    city = 'Moscow'
    context = get_data(city)
    return render(request, 'weather_forecast/index.html', context)


def get_data(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=6f9b5463e6469f3078746f08677709b4'
    weather_from_api = requests.get(url.format(city)).json()
    # print(weather_from_api)
    temperature_celsius = round(weather_from_api['main']['temp'] - 273.15)
    weather_from_api['main']['temp'] = temperature_celsius
    form = CityForm()
    context = {'weather': weather_from_api, 'form': form}
    return context
