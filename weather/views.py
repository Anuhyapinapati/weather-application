from django.shortcuts import render
import requests

def index(request):
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.POST.get('city')
        API_KEY = "7fa89c9ddda9967c068fc04c95c96eb8"  # ← replace with your key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            condition = data['weather'][0]['main'].lower()

            # choose background class based on condition
            if 'rain' in condition:
                bg_class = "rainy"
            elif 'cloud' in condition:
                bg_class = "cloudy"
            elif 'clear' in condition:
                bg_class = "sunny"
            elif 'snow' in condition:
                bg_class = "snowy"
            else:
                bg_class = "default"

            weather_data = {
                'city': city.title(),
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].title(),
                'icon': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'visibility': data.get('visibility', 0) / 1000,  # km
                'condition': condition,
                'bg_class': bg_class,
            }
        else:
            error = "City not found. Please try again."

    return render(request, 'weather/weather.html', {'weather': weather_data, 'error': error})
