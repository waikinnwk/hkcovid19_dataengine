from flask import jsonify
from app import app
from service.save_data_to_db import refresh_data
from service.get_data import *


@app.route('/refreshData')
def refresh_data_from_gov():    
    refresh_data()
    result = {"result": "OK","data": ""}
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