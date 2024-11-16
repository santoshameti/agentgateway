import requests
from typing import Dict, Any
from agentgateway.core.abstract_tool import Tool
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

class WeatherTool(Tool):
    def __init__(self):
        super().__init__("get_weather", "Get the current weather for a specified location")

    def is_auth_setup(self):
        return True

    def execute(self) -> Any:
        parameters = self.get_parameters()
        location = parameters.get('location')
        return self.get_weather_data(location)

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and country, e.g., 'London,UK'"
                }
            },
            "required": ["location"]
        }

    def get_coordinates(self, location_name):
        geolocator = Nominatim(user_agent="weather_tool")
        try:
            location = geolocator.geocode(location_name)
            if location:
                return location.latitude, location.longitude
            else:
                return None
        except (GeocoderTimedOut, GeocoderUnavailable):
            print("Error: Geocoding service is unavailable. Please try again later.")
            return None

    def get_weather_data(self, location_name):
        coordinates = self.get_coordinates(location_name)
        if not coordinates:
            return f"Unable to find coordinates for {location_name}"

        latitude, longitude = coordinates

        # API endpoint
        url = "https://api.open-meteo.com/v1/forecast"

        # Parameters for the API request
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ["temperature_2m", "precipitation", "windspeed_10m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
            "timezone": "auto",
            "forecast_days": 1
        }

        try:
            # Make the API request
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad responses
            data = response.json()

            # Extract relevant information
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            current_temp = data["hourly"]["temperature_2m"][0]
            current_precipitation = data["hourly"]["precipitation"][0]
            current_windspeed = data["hourly"]["windspeed_10m"][0]
            max_temp = data["daily"]["temperature_2m_max"][0]
            min_temp = data["daily"]["temperature_2m_min"][0]
            precipitation_sum = data["daily"]["precipitation_sum"][0]

            # Format the weather report
            weather_report = f"""
            Weather Report for {location_name} at {current_time}
            --------------------------------------
            Current Temperature: {current_temp}°C
            Current Precipitation: {current_precipitation} mm
            Current Wind Speed: {current_windspeed} km/h
            Today's Max Temperature: {max_temp}°C
            Today's Min Temperature: {min_temp}°C
            Today's Total Precipitation: {precipitation_sum} mm
            """

            return weather_report.strip()

        except requests.RequestException as e:
            return f"An error occurred while fetching weather data: {e}"
