from flask import url_for, request
import requests
import ssl
from datetime import datetime
import time


def update_building_geo_sc():
    print("update_building_geo start :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))  
    url_GetXY_Pre = "https://nominatim.openstreetmap.org/search?q="
    url_GetXY_Post = "&format=json&polygon=1&addressdetails=1"
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }    
    data_obj = []
    response_building = requests.get("https://kinhkcovid19dataengine.herokuapp.com/getBuildingWithoutGeoData",data = data_obj, headers=header)
    response_building_json_data = response_building.json()
    inserted = 0
    print("No Geo Data Building : " +str(len(response_building_json_data)))
    for building_data in response_building_json_data:
        district = building_data["district"]
        building_name = building_data["building_name"]
        try:
            response = requests.get(url_GetXY_Pre+building_name+","+district+url_GetXY_Post,data = data_obj, headers=header)
            json_data = response.json()
            for data in json_data:
                new_data_obj = {"district":district,
                    "building_name":building_name,
                    "lat": data["lat"],
                    "lon": data["lon"]}
                response = requests.post("https://kinhkcovid19dataengine.herokuapp.com/saveBuildingGEO",data = new_data_obj, headers=header)
                break
            time.sleep(1)
        except:
             print('Request except')   
    print("GEO Data added :" + str(inserted))
    print("update_building_geo end :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))  

update_building_geo_sc()

