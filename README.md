# Storm Prediction Center Geospatial Analysis Tool

## Description
This program features both current and historical forecast data from NOAA for use in weather analysis. 

## spc_main.py

This script has the user enter a city, asks them the forecast type they wish to see (categorical, tornado, wind, hail), then asks if they want the forecast for today, tomorrow, or the day after tomorrow. It then returns a brief description of the forecast based on their input.

- Uses geocoding API to convert city to usable coordinates
- Parses html to dynamically locate the .zip file (the naming convention is predictable, but a few numbers shift in the filename throughout the day)
- Extracts necessary files from .zip, and parses geospatial data from .shp files
- Generates a simple message to the user describing their forecast

### How to use spc_main.py:
Simply run the script and follow the prompts.

## spc_accuracy.py

This tool is used for analyzing the accuracy of historical forecasts. This is done by comparing forecast areas with tornado tracks, allowing the user to see whether tornadoes hit where they were forecasted to. The relation of tornado paths to forecast polygons can be used in various kinds of analysis, including finding the hit percentage of tornado paths to forecast areas (in other words, finding the general accuracy of the forecast).

Below is an example of this tool using data from the tornado outbreak on April 4, 2011. The forecast polygons are outlined in black and contain tooltips to identify the risk percentage. Tornado tracks are represented by the red lines all over the map. This appears to have been an accurate forecast, as tornado track concentration corresponds as you would expect to appropriate forecast areas.

<img width="1044" height="796" alt="Screenshot 2026-03-29 175715" src="https://github.com/user-attachments/assets/a8bcf7ce-8576-4b0a-a8dc-58792a808ee2" />


- Downloads archived forecast from a user-specified date
- Extracts .shp files from .zip, parses to obtain polygons
- Draws polygons on folium map layer by layer, labelling each polygon with the correct risk area and color scheme
- Queries a SQL db for coordinates of all tornadoes that occurred on the same user-entered date
- Draws tornadoes to the same folium map as red lines
- Overlays forecast polygons with tornado paths

### How to use spc_accuracy.py
1. Run spc_accuracy.py file and follow prompts
2. Once finished, the program will place a file called "map.html" in the "map-output" directory
3. Click on "map.html" and it should open in a web browser for you to view it


## Planned Features
- Implement ways to analyze data (for instance, generate fields in a SQL table that allow for detailed statistics)
- At a much later date, use Flask to improve presentation and user-friendliness


