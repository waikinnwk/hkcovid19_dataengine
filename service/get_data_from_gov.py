from flask import url_for, request
import requests
from service.api_config import *
from data_obj import *

def get_all_cases():
    data_obj = {}
    response = requests.get(url_for_all_cases,data = data_obj)
    json_data = response.json()
    return json_data


def get_day_summary():
    data_obj = {}
    response = requests.get(url_for_day_summary,data = data_obj)
    json_data = response.json()
    return json_data    