import requests

# API links
CITY_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true"

# Function to safely make requests and handle potential errors
def safe_get(url, params):
    try:
        response = requests.get(url, timeout=10, params=params)
        response.raise_for_status()    
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        return None

# Function to get weather data for specific city
def get_weather(city_params):

    # Make initial API request to get coordinates
    city_data = safe_get(CITY_URL, city_params)

    # Error message if city is not found
    if not city_data or not city_data.get("results"):
        print("City not found")
        return

    # Get data from API and store in variables to be used for next request
    for item in city_data["results"]:
        longitude = item["longitude"]
        latitude = item["latitude"]
        country = item["country"]
        city = item["name"]

    # Make second API request with lat and long params
    forecast_data = safe_get(FORECAST_URL, {
        "latitude": latitude,
        "longitude": longitude
    })

    # Error message if forecast is not retrieved
    if not forecast_data:
        print("Failed to retrieve forecast")
        return
    
    # Return dict with all variables needed to print result
    return {
        "city": city,
        "country": country,
        "longitude": forecast_data["longitude"],
        "latitude": forecast_data["latitude"],
        "elevation": forecast_data["elevation"],
        "temperature": forecast_data["current_weather"]["temperature"],
        "windspeed": forecast_data["current_weather"]["windspeed"],
        "time": forecast_data["current_weather"]["time"]
    }

# WeatherReport class for later to save multiple instances/reports at once
# __str__ also allows for nice printing of result
class WeatherReport:
    def __init__(self, data):
        self.city = data['city']
        self.country = data['country']
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.elevation = data['elevation']
        self.temperature = data['temperature']
        self.windspeed = data['windspeed']
        self.time = data['time']

    def __str__(self):
        return (
            f"\n~~~ Weather Report ~~~\n"
            f"City:        {self.city}, {self.country}\n"
            f"Coordinates: {self.latitude}°N, {self.longitude}°E\n"
            f"Elevation:   {self.elevation} m\n"
            f"Temperature: {self.temperature}°C\n"
            f"Wind Speed:  {self.windspeed} km/h\n"
            f"Time:        {self.time}\n"
            f"{"~" * 20}"
        )

    def __repr__(self):
        return (
        f"WeatherReport(data={{"
        f"'city': {self.city}, "
        f"'country': {self.country}, "
        f"'latitude': {self.latitude}, "
        f"'longitude': {self.longitude}, "
        f"'elevation': {self.elevation}, "
        f"'temperature': {self.temperature}, "
        f"'windspeed': {self.windspeed}, "
        f"'time': {self.time}"
        f"}})"
    )


