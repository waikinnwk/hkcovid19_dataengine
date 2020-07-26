import time
from datetime import datetime
from db import db
from service.api_config import *
from service.get_data_from_gov import *
from data_obj.case import *
from data_obj.day_summary import *
from data_obj.related_building import *

def refresh_data():
    print("refresh_data start :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    cases = get_all_cases()
    for case in cases:
        case_from_db = Case.query.get(int(case[case_no_key]))
        if(case_from_db is None):
            report_date_str = ""
            for c in case[report_date_key]:
                if c =='/' or c.isnumeric():
                    report_date_str += c
            new_case = Case(case_no=int(case[case_no_key]),
                report_date = datetime.strptime(report_date_str, data_format).replace(hour=0, minute=0, second=0, microsecond=0),
                onset_date = case[onset_date_key],
                gender = case[gender_key],
                age = int(case[age_key]),
                admitted_hospital = case[admitted_hospital_key],
                hospital_status = case[hospital_status_key],
                is_hk_resident = case[is_hk_resident_key],
                case_classification = case[case_classification_key],
                status = case[status_key])           
            try:
                db.session.add(new_case)
                db.session.commit()
            except:
                print('Error')    
    day_summarys = get_day_summary()
    for day_summary in day_summarys:
        day_summary_from_db = DaySummary.query.get(day_summary[as_of_date_key])
        if(day_summary_from_db is None):
            new_day_summary = DaySummary(as_of_date=day_summary[as_of_date_key],
                no_of_confirmed_cases=day_summary[no_of_confirmed_cases_key],
                no_of_ruled_out_cases = day_summary[no_of_ruled_out_cases_key],
                no_of_cases_still_hospitalised_for_investigation = day_summary[no_of_cases_still_hospitalised_for_investigation_key],
                no_of_cases_fulfilling_the_reporting_criteria = day_summary[no_of_cases_fulfilling_the_reporting_criteria_key],
                no_of_death_cases=day_summary[no_of_death_cases_key],
                no_of_discharge_cases = day_summary[no_of_discharge_cases_key],
                no_of_probable_cases = day_summary[no_of_probable_cases_key],
                no_of_hospitalised_cases_in_critical_condition = day_summary[no_of_hospitalised_cases_in_critical_condition_key]
            )
            try:
                db.session.add(new_day_summary)
                db.session.commit()
            except:
                print('Error')   
    
    print("refresh_data end :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


