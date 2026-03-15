import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup
import re

def download_zip_file():
    # STEP 2: a zip file for download is located, utilizing knowledge of the SPC's predictable URL naming conventions
    first_half_url = "https://www.spc.noaa.gov/products/outlook/"
    day1_url = requests.get(first_half_url + "day1otlk.html") 
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
    
if __name__ == "__main__":
    download_zip_file()
