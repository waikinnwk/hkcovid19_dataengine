from flask import url_for, request
import requests
import ssl
from datetime import datetime
import time
from service.save_data_to_db import save_building_geo

def get_building_geo_to_local():
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }       
    data_obj = []
    building = requests.get("https://kinhkcovid19dataengine.herokuapp.com/getBuildingGeoData",data = data_obj, headers=header)
    building_json_data = building.json()
    print("No Geo Data Building : " +str(len(building_json_data)))
    for building_data in building_json_data:
        district = building_data["district"]
        building_name = building_data["building_name"]
        lat = building_data["lat"]
        lon = building_data["lon"]
        save_building_geo(district,building_name,lat,lon)


