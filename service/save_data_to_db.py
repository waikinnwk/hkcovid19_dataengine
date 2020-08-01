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
        report_date_str = ""
        for c in day_summary[as_of_date_key]:
            if c =='/' or c.isnumeric():
                report_date_str += c
        day_summary_from_db = DaySummary.query.get(datetime.strptime(report_date_str, data_format).replace(hour=0, minute=0, second=0, microsecond=0))
        if(day_summary_from_db is None):

            new_day_summary = DaySummary(as_of_date=datetime.strptime(report_date_str, data_format).replace(hour=0, minute=0, second=0, microsecond=0),
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
    
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    related_buildings = get_related_buildings()
    for related_building in related_buildings:
        related_building_from_db = RelatedBuilding.query.filter(RelatedBuilding.as_of_date == today).filter(RelatedBuilding.building_name == related_building[building_name_key]).first()
        related_case = related_building[related_case_key]
        no_of_case = 0
        if(len(related_case) > 0):
            no_of_case = len(related_case.split(","))
        if(related_building_from_db is None):
            new_related_building = RelatedBuilding(as_of_date=today,
                district=related_building[district_key],
                building_name = related_building[building_name_key],
                last_date_of_residence_of_the_case = related_building[last_date_of_residence_of_the_case_key],
                related_case = related_building[related_case_key],
                no_of_case = no_of_case
            )
            try:
                db.session.add(new_related_building)
                db.session.commit()
            except:
                print('Error')   
        else:
            if related_building_from_db.last_date_of_residence_of_the_case != related_building[last_date_of_residence_of_the_case_key] and related_building_from_db.related_case != related_building[related_case_key]:
                related_building_from_db.last_date_of_residence_of_the_case = related_building[last_date_of_residence_of_the_case_key]
                related_building_from_db.related_case = related_building[related_case_key]
                related_building_from_db.no_of_case = no_of_case
                try:
                    db.session.add(new_related_building)
                    db.session.commit()
                except:
                    print('Error')   


    print("refresh_data end :" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


