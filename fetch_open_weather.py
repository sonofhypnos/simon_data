import os
import requests
import json
from datetime import datetime, timedelta

days_since = 29  # How many days back do you want to get data?
days_forward = 29

# load .env manually, because dotenv is so crappy it can't even be installed
# without giving me problems in pip
def load_env(file_path):
    with open(file_path, "r") as file:
        for line in file:
            key_value = line.strip().split("=", 1)
            if len(key_value) == 2:
                os.environ[key_value[0].strip()] = key_value[1].strip()


# Assuming '.env' is in the current directory
load_env(".env")

weather_api_key = os.getenv("WEATHER_API_KEY")

# Function to make API calls and fetch weather data
def fetch_weather_data(lat, lon, date, api_key):
    timestamp = int(datetime.timestamp(date))
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}"
    response = requests.get(url)
    return response.json()


# Main function to fetch and save weather data for the last two months
def save_weather_data():
    api_key = weather_api_key  # Replace with your actual API key
    lat = 47.1167
    lon = 13.1333
    start_date = datetime.now() - timedelta(days=days_since)
    data = []
    end_date = start_date + timedelta(days=days_forward)

    for day in range(days_forward):
        for hour in range(24):
            date = start_date + timedelta(days=day, hours=hour)
            daily_data = fetch_weather_data(lat, lon, date, api_key)
            data.append(daily_data)
            print(f"Data for {date.strftime('%Y-%m-%d')} fetched successfully.")
            print(data)

    date_formatting = "%Y-%m-%d"
    # Save the data to a JSON file
    with open(
        f"data/weather/weather_data_{start_date.strftime(date_formatting)}_{end_date.strftime(date_formatting)}.json",
        "w",
    ) as file:
        json.dump(data, file)

    print("All data saved to weather_data.json")


# Run the function
save_weather_data()
