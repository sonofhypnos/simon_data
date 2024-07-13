import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


days_since = 73  # How many days back do you want to get data?
api_key = os.getenv("WEATHER_API_KEY")


# Function to make API calls and fetch weather data
def fetch_weather_data(lat, lon, date, api_key):
    timestamp = int(datetime.timestamp(date))
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}"
    response = requests.get(url)
    return response.json()


# Main function to fetch and save weather data for the last two months
def save_weather_data():
    api_key = "your_api_key_here"  # Replace with your actual API key
    lat = 47.1167
    lon = 13.1333
    start_date = datetime.now() - timedelta(days=days_since)
    data = []

    for day in range(60):
        date = start_date + timedelta(days=day)
        daily_data = fetch_weather_data(lat, lon, date, api_key)
        data.append(daily_data)
        print(f"Data for {date.strftime('%Y-%m-%d')} fetched successfully.")

    # Save the data to a JSON file
    with open("weather_data.json", "w") as file:
        json.dump(data, file)

    print("All data saved to weather_data.json")


# Run the function
save_weather_data()
