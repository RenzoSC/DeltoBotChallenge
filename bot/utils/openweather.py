import requests
from settings import OPENWEATHER_API_KEY

def get_weather(city: str) -> dict:
    """Get the weather for a city. Returns a dictionary with the weather data in spanish."""
    
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es"
    response = requests.get(api_url)
    json_response = response.json()
    
    return json_response