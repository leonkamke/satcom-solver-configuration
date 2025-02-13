import requests
from datetime import datetime

def fetch_weather_data_with_cloud_coverage(latitude, longitude, date):
    # Base URL for the Open-Meteo API
    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date,
        "end_date": date,
        "daily": "sunshine_duration,sunrise,sunset",
        "timezone": "auto"
    }
    
    # Make the request
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    
    # Parse the JSON response
    data = response.json()
    
    # Extract relevant data
    sunrise = data["daily"]["sunrise"][0]
    sunset = data["daily"]["sunset"][0]
    sunshine_duration = data["daily"]["sunshine_duration"][0]  # In seconds

    # Convert sunrise and sunset to datetime objects
    sunrise_time = datetime.fromisoformat(sunrise)
    sunset_time = datetime.fromisoformat(sunset)

    # Calculate the duration between sunrise and sunset in seconds
    daylight_duration_seconds = (sunset_time - sunrise_time).seconds

    # Calculate cloud coverage (1 - sunshine_duration / daylight_duration)
    cloud_coverage = 1 - (sunshine_duration / daylight_duration_seconds)
    
    # Convert sunshine duration to hours for easier interpretation
    sunshine_duration_hours = sunshine_duration / 3600

    return {
        "date": date,
        "latitude": latitude,
        "longitude": longitude,
        "sunrise": sunrise,
        "sunset": sunset,
        "sunshine_duration_hours": sunshine_duration_hours,
        "daylight_duration_hours": daylight_duration_seconds / 3600,  # Convert seconds to hours
        "cloud_coverage_fraction": cloud_coverage  # Value between 0 (clear) and 1 (fully cloudy)
    }

# Example usage
latitude = 60
longitude = -1.0
date = "2021-05-02"

weather_data = fetch_weather_data_with_cloud_coverage(latitude, longitude, date)
print(weather_data)
