from flask import jsonify
from app import app
from service.save_data_to_db import refresh_data,update_building_geo,save_building_geo
from service.save_data_to_db_local import get_building_geo_to_local
from service.get_data import *
from flask import request

@app.route('/refreshData')
def refresh_data_from_gov():    
    refresh_data()
    result = {"result": "OK","data": ""}
    return jsonify(result)

@app.route('/updateBuildingGEO')
def update_buidling_geo_p():    
    update_building_geo()
    result = {"result": "OK","data": ""}
    return jsonify(result)

@app.route('/saveBuildingGEO', methods=['POST'])
def save_buidling_geo():    
    district = request.values.get("district")
    building_name = request.values.get("building_name")
    lat = request.values.get("lat")
    lon = request.values.get("lon")
    save_building_geo(district,building_name,lat,lon)
    result = {"result": "OK","data": ""}
    return jsonify(result)

@app.route('/getNoOfPage', methods=['POST'])
def get_no_of_page():
    record_per_page = int(request.values.get("record_per_page"))
    page = get_case_no_of_page(record_per_page)
    result = {}
    result["no_of_page"] = page
    return jsonify(result)  
    

@app.route('/getCasesByPage', methods=['POST'])
def get_cases_by_page():     
    page = int(request.values.get("page")) -1
    record_per_page = int(request.values.get("record_per_page"))
    result = get_case_by_page(page,record_per_page)
    return jsonify(result)    

@app.route('/getCaseNoByMonth', methods=['POST'])
def caseno_by_month():
    result = get_caseno_by_month_from_db()
    return jsonify(result)


@app.route('/getCaseGroupByAge', methods=['POST'])
def get_case_group_by_age():
    return jsonify(get_case_group_by_age_from_db())


@app.route('/getSymptomaticResult', methods=['POST'])
def get_symptomatic_result():
    symptomatic_result = get_case_by_symptomatic_from_db()
    return jsonify(symptomatic_result)

@app.route('/getLatestSummary', methods=['POST'])
def get_latest_summary():
    return jsonify(get_latest_summary_from_db())


@app.route('/getSummaryForPast14', methods=['POST'])
def get_summary_for_past_14():
    return jsonify(get_summary_for_past_14_from_db())

@app.route('/getRelatedBuildings', methods=['POST'])
def get_related_budilings():
    return jsonify(get_latest_related_building_from_db())

@app.route('/getDistrictData', methods=['POST'])
def get_district_data():
    return jsonify(get_latest_district_data_from_db())


@app.route('/getBuildingGeoData')
def get_building_geo_data():
    return jsonify(get_building_geo_data_from_db())

@app.route('/getBuildingWithoutGeoData')
def get_building_without_geo_data():
    return jsonify(get_building_without_geo_data_from_db())
    

@app.route('/refreshGeoDataFromHerokuToLocal')
def refresh_geo_data_to_local():    
    get_building_geo_to_local()
    result = {"result": "OK","data": ""}
    return jsonify(result)