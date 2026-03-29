import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup
import re
from shapely.geometry import Point
import geopandas as gpd
from local_forecast import LocalForecast
import os

def city_to_coordinates(city):
    # STEP 1: a city is converted to coordinates in this function
    url = "https://nominatim.openstreetmap.org/search?"
    params = "addressdetails=1&q=" + city.replace(" ", "+") + "&format=jsonv2"
    full_url = url + params
    response = requests.get(full_url, headers={"User-Agent": "SPCapp (dastardlycakev4@gmail.com)"})
    json = response.json()

    lat = json[0]['lat']
    lon = json[0]['lon']

    return {"latitude": lat, "longitude": lon, "city-name": city}

def download_zip_file(which_day):
    # STEP 2: a zip file for download is located, utilizing knowledge of the SPC's predictable URL naming conventions
    first_half_url = "https://www.spc.noaa.gov/products/outlook/"
    day1_url = requests.get(first_half_url + "day" + which_day + "otlk.html") 
    day1_url_parsing = BeautifulSoup(day1_url.content, "html.parser")

    #html is parsed on the forecast page for the name of .shp file archive
    for tags in day1_url_parsing.find_all("a"):
        string_of_tags = str(tags)
        if "shp.zip" in string_of_tags:
            url_start = re.search("archive",string_of_tags).start()
            url_end = re.search("zip", string_of_tags).end() 
            second_half_url = (string_of_tags[url_start:url_end])
    
    shp_file_location = requests.get(first_half_url + second_half_url) #the entire URL of the .shp file archive is obtained and downloaded
    with open("spcdata.zip", mode="wb") as file:
        file.write(shp_file_location.content)


def zip_file_iteration(user_specified_outlook):
    # STEP 3: iterate over contents of downloaded .zip file, making sure to only extract what is necessary based on user's specification
    with ZipFile("spcdata.zip", 'r') as myzip:
        file_list = myzip.namelist()
        
        # only necessary files are extracted based on desired outlook
        for i in file_list:
            if user_specified_outlook == "categorical" and "cat" in i:
                if "shp" in i:
                    name_of_desired = i
                myzip.extract(i)
            if user_specified_outlook == "hail" and not "sig" in i and "hail" in i:
                if "shp" in i:
                    name_of_desired = i
                myzip.extract(i)
            if user_specified_outlook == "tornado" and not "sig" in i and "torn" in i:
                if "shp" in i:
                    name_of_desired = i
                myzip.extract(i)
            if user_specified_outlook == "wind" and not "sig" in i and "wind" in i:
                if "shp" in i:
                    name_of_desired = i
                myzip.extract(i)

        return name_of_desired
    
def shape_file_parsing():
    # STEP 4: the .shp file extracted from earlier is parsed and used to tell the user what risk area their specified city is in
    city = city_to_coordinates(input("Enter a city: "))
    outlook_type = input(
        "Which type of outlook do you wish to view? (categorical,tornado,hail,wind): ").lower().strip()

    # loop handles bad input
    accepted_input = ("categorical", "tornado", "hail", "wind")
    while outlook_type not in accepted_input:
        outlook_type = input(
            "Input not accepted. Which type of outlook do you wish to view? (categorical,tornado,hail,wind): ").lower().strip()

    if outlook_type != "categorical":
        which_day = input("Choose which day's outlook (1, 2): ")
    else:
        which_day = input("Choose which day's outlook (1, 2, 3): ")
    download_zip_file(which_day)
    name_of_file = zip_file_iteration(outlook_type)

    try:
        shape_file = gpd.read_file(name_of_file).to_crs(crs=4326, epsg=4326)
    except ValueError:
        print(r"Less than 2% risk for all areas.")
        return
    
    shape_dict = shape_file.to_geo_dict()
    gdf = gpd.GeoDataFrame.from_features(shape_dict["features"])  # the features (ie coordinates) from the extacted shp file are accessed
    
    coord_to_use = gpd.GeoSeries([Point(city["longitude"], city["latitude"])], crs="EPSG:3857")

    #occasionally, risk types will contain a special conditional risk on top of the general forecast. A list exists to hold multiple risk types if there are more than one
    risk_exists = False
    all_risks = []
    for num, i in enumerate(gdf.contains(coord_to_use[0])):
        if i == True:
            num_caught = num
            all_risks.append(num_caught)
            risk_exists = True

    risk_type = []
    if not risk_exists:
        print("No storm risks today")
    else:
        for risk_id in all_risks:
            risk_type.append(gdf.loc[risk_id, "LABEL2"])
    
    if len(risk_type) > 0:
        risk_types = " and ".join(risk_type)
    else:
        risk_types = "No risk"

    print(f"User selected day {which_day} {outlook_type} outlook. {risk_types} exists in {str.capitalize(city['city-name'])}.")
    
    return LocalForecast(outlook_type, risk_type, city["city-name"])

if __name__ == "__main__":
    shape_file_parsing()
    
    disposable_extensions = (".shp", ".shx", ".dbf", ".prj", ".zip")
    for file in os.listdir():
        if file.endswith(disposable_extensions):
            os.remove(file)
