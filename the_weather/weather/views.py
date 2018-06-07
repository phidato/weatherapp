from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
	cities = City.objects.all()
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f00f4349940a6ccde3867f0b33979504'
	if request.method == 'POST': # only true if form is submitted
		form = CityForm(request.POST) # add actual request data to form for processing
		form.save() # will validate and save if validate

	form = CityForm()
	weather_data = []
	
	for city in cities:
		city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
		weather = {
			'city' : city,
			'temperature' : city_weather['main']['temp'],
			'description' : city_weather['weather'][0]['description'],
			'icon' : city_weather['weather'][0]['icon']
		}
		weather_data.append(weather)
	
	context = {'weather_data' : weather_data, 'form' : form}
	
	import pdb
	print (context)
	return render(request,'weather/index.html',context)
