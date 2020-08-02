import os
ON_HEROKU = os.environ.get('ON_HEROKU')

if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995
else:
    port = 5000


from flask import url_for, request
import requests

url = "http://localhost:"+str(port)+"/updateBuildingGEO"

data_obj = {}
response = requests.get(url,data = data_obj)
json_data = response.json()

print(json_data)