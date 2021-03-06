from flask import url_for, request, jsonify
import requests
import ssl
from datetime import datetime
import time
import os
backend_url = os.environ.get('backend_url')
google_api_key = os.environ.get('google_api_key')
if backend_url is None:
    backend_url = 'https://kinhkcovid19dataengine.herokuapp.com/'


def update_building_geo_sc():
    print("update_building_geo start :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))  
    url_GetXY_Pre = "https://nominatim.openstreetmap.org/search?q="
    url_GetXY_Post = "&format=json&polygon=1&addressdetails=1"

    url_GetXY_Pre_google ="https://maps.googleapis.com/maps/api/geocode/json?address="
    url_GetXY_Post_google = ",Hong Kong&key=" + google_api_key

    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }    
    data_obj = []
    response_building = requests.get(backend_url + "getBuildingWithoutGeoData",data = data_obj, headers=header)
    response_building_json_data = response_building.json()
    inserted = 0
    print("No Geo Data Building : " +str(len(response_building_json_data)))
    for building_data in response_building_json_data:
        district = building_data["district"]
        building_name = building_data["building_name"]
        try:
            map_request_starttime = datetime.now()
            response = requests.get(url_GetXY_Pre+building_name+","+district+url_GetXY_Post,data = data_obj, headers=header)
            json_data = response.json()
            if len(json_data) > 0:           
                for data in json_data:
                    new_data_obj = {"district":district,
                        "building_name":building_name,
                        "lat": data["lat"],
                        "lon": data["lon"]}
                    response = requests.post(backend_url + "/saveBuildingGEO",data = new_data_obj, headers=header)
                    inserted+=1
                    print('Updated by Open Street:' + str(inserted))   
                    break
            else:
                print("No result from Open Street Map - Go for Google")
                urlToGoogle = url_GetXY_Pre_google+building_name+","+district+url_GetXY_Post_google
                response = requests.get(urlToGoogle,data = data_obj, headers=header)
                json_data = response.json()
                result_data = json_data["results"]
                if len(result_data) > 0:
                    for data in result_data:
                        geometry = data["geometry"]
                        location = geometry["location"]
                        new_data_obj = {"district":district,
                        "building_name":building_name,
                        "lat": location["lat"],
                        "lon": location["lng"]}
                        response = requests.post(backend_url + "/saveBuildingGEO",data = new_data_obj, headers=header)
                        inserted+=1
                        print('Updated by Google:' + str(inserted))   
                        break
                else:
                    print("No result from Open Street Map & Google " + building_name +","+district)
                    new_data_obj = {"district":district,
                    "building_name":building_name}
                    response = requests.post(backend_url + "/saveEmptyBuildingGEO",data = new_data_obj, headers=header)
                    inserted+=1
                    print('Updated Empty GEO:' + str(inserted))  

        except:
             print('Request except')   
        if inserted >= 150:
            break
        else:
            map_request_endtime = datetime.now()
            difference = (map_request_endtime - map_request_starttime)
            total_seconds = difference.total_seconds()        
            if total_seconds < 1:
                time.sleep(1)
    print("GEO Data added :" + str(inserted))
    print("update_building_geo end :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))  

update_building_geo_sc()

