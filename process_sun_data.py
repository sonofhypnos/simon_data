import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

start_of_workday = 8
end_of_workday = 13


def estimate_sun_hour(hour_data):
    dt = datetime.fromtimestamp(hour_data["dt"])
    sunrise = datetime.fromtimestamp(hour_data["sunrise"])
    sunset = datetime.fromtimestamp(hour_data["sunset"])

    if sunrise <= dt <= sunset:
        cloud_cover = hour_data["clouds"]
        # Estimate sun hour based on cloud cover
        return 1 - (cloud_cover / 100)
    return 0


def process_weather_data_to_csv(input_files, output_file, daily_output_file):
    hourly_data = defaultdict(lambda: defaultdict(float))

    for input_file in input_files:
        with open(input_file, "r") as json_file:
            data = json.load(json_file)
            for entry in data:
                hour_data = entry["data"][
                    0
                ]  # Access the single entry in the 'data' list

                dt = datetime.fromtimestamp(hour_data["dt"])
                date = dt.strftime("%Y-%m-%d")
                hour = dt.strftime("%H")

                sun_hour = estimate_sun_hour(hour_data)
                hourly_data[date][hour] = max(
                    hourly_data[date][hour], sun_hour
                )  # Keep the maximum value in case of duplicates

    # Write hourly data
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Hour", "Estimated Sun Hour"])

        for date in sorted(hourly_data.keys()):
            for hour in sorted(hourly_data[date].keys()):
                writer.writerow([date, hour, round(hourly_data[date][hour], 2)])

    print("Hourly CSV file has been created with estimated sun hours.")

    # Aggregate and write daily data
    with open(daily_output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Total Estimated Sun Hours"])

        for date in sorted(hourly_data.keys()):
            total_sun_hours = 0
            for hour in hourly_data[date]:
                if int(hour) >= start_of_workday and int(hour) <= end_of_workday:
                    total_sun_hours += hourly_data[date][hour]
            writer.writerow([date, round(total_sun_hours, 2)])

    print("Daily CSV file has been created with aggregated sun hours.")


# Specify the input JSON files and output CSV file paths
input_json_files = [
    # NOTE: duplicate data does not lead to problems. Data should overlap by 2 days (or you need to pay close attention until which hour the data goes)
    "data/weather/weather_data_2024-05-01_2024-06-01.json",
    "data/weather/weather_data_2024-06-01_2024-07-01.json",
    "data/weather/weather_data_2024-06-30_2024-07-29.json",
    "data/weather/weather_data_2024-07-08_2024-08-06.json",
    "data/weather/weather_data_2024-07-30_2024-08-31.json",
    "data/weather/weather_data_2024-08-25_2024-09-23.json",
]
output_csv_file = "data/weather/estimated_hourly_sun_hours.csv"
daily_output_csv_file = "data/weather/estimated_daily_sun_hours_during_work.csv"

# Call the function to process the data
process_weather_data_to_csv(input_json_files, output_csv_file, daily_output_csv_file)
