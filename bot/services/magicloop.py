import requests
from settings import MAGICLOOP_WEATHER_FUNCTION_KEY

def get_weather_analisis(weather_info: dict) -> str:
    """
    Calls the MagicLoop API to get the weather analysis.

    Args:
    - weather_info: A dictionary with the weather information.

    Returns:
    - A string with the weather analysis.
    """
    url = f'https://magicloops.dev/api/loop/{MAGICLOOP_WEATHER_FUNCTION_KEY}/run'
    response = requests.post(url, json=weather_info)

    json_response = response.json()
    return json_response