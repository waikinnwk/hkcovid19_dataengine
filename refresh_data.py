from flask import url_for, request
import requests

url = "https://kinhkcovid19dataengine.herokuapp.com/refreshData"

data_obj = {}
response = requests.get(url,data = data_obj)
json_data = response.json()

print(json_data)