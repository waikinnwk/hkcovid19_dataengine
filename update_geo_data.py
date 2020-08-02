from app import db
from data_obj.building_geo import *
from data_obj.related_building import *
import requests
import ssl
from datetime import datetime
import time
from util.utils import convert_building_name_to_geo


def update_building_geo_sc():
    print("update_building_geo start :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))  
    url_GetXY_Pre = "https://nominatim.openstreetmap.org/search?q="
    url_GetXY_Post = "&format=json&polygon=1&addressdetails=1"
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }    
    data_obj = []
    related_buildings = RelatedBuilding.query.order_by(RelatedBuilding.district).all()
    skip = 0
    inserted = 0
    for related_building in related_buildings:
        trim_building_name = convert_building_name_to_geo(related_building.building_name)
        building_geo_from_db = BuildingGeoInfo.query.filter(BuildingGeoInfo.district == related_building.district).filter(BuildingGeoInfo.building_name == trim_building_name).first()
        if not building_geo_from_db :
            try:
                response = requests.get(url_GetXY_Pre+trim_building_name+","+related_building.district+url_GetXY_Post,data = data_obj, headers=header)
                json_data = response.json()
                for data in json_data:
                    new_building_geo = BuildingGeoInfo(
                        district=related_building.district,
                        building_name = trim_building_name,
                        lat = data["lat"],
                        lon = data["lon"]
                    )
                    try:
                        db.session.add(new_building_geo)
                        db.session.commit()
                        inserted+=1
                        print('GEO inserted')    
                        break
                    except:
                        print('DB except')    
                time.sleep(1)
            except:
                print('Request except')   
        else:
            skip+=1
    print("GEO Data added :" + str(inserted) + "| skipped" + str(skip))
    print("update_building_geo end :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))  

update_building_geo_sc()