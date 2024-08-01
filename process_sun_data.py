import json
import csv
from datetime import datetime

# Function to estimate sun hours based on cloud cover throughout the day
def estimate_sun_hours(hourly_data):
    sun_hours = 0
    for hour in hourly_data:
        cloud_cover = hour["clouds"]
        # Simplified assumption: less cloud cover = more sun hours
        sun_hours += 1 - cloud_cover / 100
    return sun_hours


# Function to read the weather data from JSON and write estimated sun hours to a CSV file
def process_hourly_data_to_csv(input_file, output_file):
    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Estimated Sun Hours"])

        for daily_data in data:
            if "hourly" in daily_data:  # Ensure hourly data is present
                date = datetime.fromtimestamp(daily_data["hourly"][0]["dt"]).strftime(
                    "%Y-%m-%d"
                )
                sun_hours = estimate_sun_hours(daily_data["hourly"])
                writer.writerow([date, sun_hours])

        print("CSV file has been created with estimated sun hours.")


# Specify the input JSON file and output CSV file paths
input_json_file = "weather_data.json"
output_csv_file = "estimated_sun_hours.csv"

# Call the function to process the data
process_hourly_data_to_csv(input_json_file, output_csv_file)
