Manual created: 2024-07-04

Thermometer code needs the python env .env3.9, because 3.10 is not supported.
Other code uses normal .env/

Explanation:
- Has analysis and data for simons productivity data
- the ground truth for simons productivity data is supposed to stay the online google sheets file. We only read and wrangle this data for analysis
- has code to extract and modify RC-5 thermometer (this code did not end up working due to hardware issues that could never be resolved)
- has a weather script to get data from open_weather.

# General information:
- There are two main downstream 'variables' that interest us: Simon's sleep and Simon's productivity.
- There are two functions to calculate effects for each of these variables respectively. The notebook also has a lot of cells for data cleaning and formatting in the beginning

# How to update the open weather data
Info:
- openweather allows a limit of 1K api calls per day. Since 24*30=720, you can only download 1 day worth of api calls for free per day. You also need an api key from them to run these functions at all I believe. The repository has code to fetch the api key from the ignored .env file.

Steps:
- [ ] download data (until you have all data for last months)
 - [ ] open `fetch_open_weather.py`
 - [ ] change the variables for `days_since`, and `days_forward` to determine for which time_window you want to download data
 - [ ] check if the coordinates specified in the file still apply to simon's current location
 - [ ] run `fetch_open_weather.py` (Make sure your data overlaps by 2 days with previous data or you might get missing data within 1 day!)
- [ ] turn the data to csv data:
  - [ ] open `process_sun_data.py`
  - [ ] add your files to the `input_json_files` variable
  - [ ] run `process_sun_data.py`
  - [ ] possibly there is duplicate data that you need to manually deal with?


