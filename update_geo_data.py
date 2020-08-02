from app import db

from data_obj.building_geo import *
from data_obj.related_building import *
import requests
import ssl
from datetime import datetime
import time
from util.utils import convert_building_name_to_geo
from sqlalchemy import *


def update_building_geo_sc():
    print("update_building_geo start :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))  
    url_GetXY_Pre = "https://nominatim.openstreetmap.org/search?q="
    url_GetXY_Post = "&format=json&polygon=1&addressdetails=1"
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }    
    data_obj = []
    related_buildings = RelatedBuilding.query.filter(
        ~BuildingGeoInfo.query
        .filter(BuildingGeoInfo.district == RelatedBuilding.district)
        .filter(BuildingGeoInfo.building_name == func.trim(func.replace(func.upper(RelatedBuilding.building_name),'(NON-RESIDENTIAL)','')))
        .exists()
    ).order_by(RelatedBuilding.district).all()
    inserted = 0
    print("No Geo Data Building : " +str(len(related_buildings)))
    for related_building in related_buildings:
        try:
            response = requests.get(url_GetXY_Pre+trim_building_name+","+related_building.district+url_GetXY_Post,data = data_obj, headers=header)
            json_data = response.json()
            for data in json_data:
                new_data_obj = {"district":related_building.district,
                    "building_name":trim_building_name,
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

