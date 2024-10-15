import os
import requests
import urllib.parse

def lookup_weather(city=None, lat=None, lon=None):
    """Look up current weather by city name or coordinates."""
    try:
        api_key = os.environ.get("API_KEY")
        if city:
            url = f'https://api.weatherbit.io/v2.0/current?city={urllib.parse.quote_plus(city)}&key={api_key}'
        elif lat and lon:
            url = f'https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={api_key}'
        else:
            return None

        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
                    

    try:
        data = response.json()
        weather_info = {
            "city": data["data"][0]["city_name"],
            "temperature": data["data"][0]["temp"],
            "feels_like": data["data"][0]["app_temp"],
            "description": data["data"][0]["weather"]["description"],
            "wind_speed": data["data"][0]["wind_spd"],
            "humidity": data["data"][0]["rh"],
            "aqi": data["data"][0]["aqi"],
            "ob_time": data["data"][0]["ob_time"],
        }
        return weather_info
    except (KeyError, TypeError, ValueError):
        return None

def lookup_forecast(city):
    """Look up 16-day weather forecast for a city."""
    try:
        api_key = os.environ.get("API_KEY")
        url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={urllib.parse.quote_plus(city)}&key={api_key}'
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        data = response.json()
        forecast_data = []
        for day in data["data"]:
            day_forecast = {
                "date": day["datetime"],
                "max_temp": day["max_temp"],
                "min_temp": day["min_temp"],
                "description": day["weather"]["description"],
                "precip": day["precip"],
                "uv": day["uv"],
                "wind_speed": day["wind_spd"],
                "wind_direction": day["wind_cdir_full"],
            }
            forecast_data.append(day_forecast)
        return forecast_data
    except (KeyError, TypeError, ValueError):
        return None




# Make sure API key is set
if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
