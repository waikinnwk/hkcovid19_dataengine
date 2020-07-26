import json
from data_obj.case import *
from data_obj.day_summary import *
from datetime import datetime, timedelta
from db import db
from sqlalchemy import *

def get_case_group_by_age_from_db():
    cases = Case.query.order_by(Case.case_no).all()
    case_label = ["below 18","18-30","31-40","41-50","51-65","over 65"]
    case_data_map = {"below 18":0,"18-30":0,"31-40":0,"41-50":0,"51-65":0,"over 65":0}
    for case in cases:
        if case.age < 18:
            case_data_map["below 18"] +=1  
        elif case.age >=18 and case.age <=30:
            case_data_map["18-30"] +=1  
        elif case.age >=31 and case.age <=40:
            case_data_map["31-40"] +=1  
        elif case.age >=41 and case.age <=50:
            case_data_map["41-50"] +=1  
        elif case.age >=51 and case.age <=65:
            case_data_map["51-65"] +=1  
        elif case.age > 65:
            case_data_map["over 65"] +=1  
    case_data = [case_data_map["below 18"],case_data_map["18-30"],case_data_map["31-40"],case_data_map["41-50"],case_data_map["51-65"],case_data_map["over 65"]]

    result = {"label": case_label,"data": case_data}
    return result


def get_caseno_by_month_from_db():
    cases = Case.query.order_by(Case.case_no).all()
    local_case_data_map = {}
    import_case_data_map = {}
    total_local_case = 0
    total_import_case = 0
    for case in cases:
        data_month_gp = str(case.report_date.year) + "-" + str(case.report_date.month)
        if(case.case_classification == 'Imported case'):
            if data_month_gp in import_case_data_map:
                import_case_data_map[data_month_gp] +=1  
            else:
                import_case_data_map[data_month_gp] = 1    
            total_import_case +=1
        else:
            if data_month_gp in local_case_data_map:
                local_case_data_map[data_month_gp] +=1  
            else:
                local_case_data_map[data_month_gp] = 1     
            total_local_case +=1 

    for key in local_case_data_map:
        if key not in import_case_data_map:
            import_case_data_map[key] = 0


    for key in import_case_data_map:
        if key not in local_case_data_map:
            local_case_data_map[key] = 0    
    
    result = {
        "local_case_data_map" : local_case_data_map,
        "import_case_data_map" : import_case_data_map,
        "total_local_case" : total_local_case,
        "total_import_case" : total_import_case       
    }

    return result


def get_case_by_symptomatic_from_db():
    cases = Case.query.order_by(Case.case_no).all()
    symptomatic_case = 0
    asymptomatic_case = 0
    for case in cases:
        if case.onset_date == 'Asymptomatic':
            asymptomatic_case +=1
        else:
            symptomatic_case +=1

    result = {
        "asymptomatic_case" : asymptomatic_case,
        "symptomatic_case" : symptomatic_case     
    }

    return result

def get_latest_summary_from_db(): 

    daysummary = DaySummary.query.order_by(DaySummary.as_of_date.desc()).first()
    result = {}
    result["as_of_date"] = daysummary.as_of_date.strftime("%d/%m/%Y")
    result["no_of_confirmed_cases"] = daysummary.no_of_confirmed_cases
    result["no_of_ruled_out_cases"] = daysummary.no_of_ruled_out_cases
    result["no_of_cases_still_hospitalised_for_investigation"] = daysummary.no_of_cases_still_hospitalised_for_investigation
    result["no_of_cases_fulfilling_the_reporting_criteria"] = daysummary.no_of_cases_fulfilling_the_reporting_criteria
    result["no_of_death_cases"] = daysummary.no_of_death_cases
    result["no_of_discharge_cases"] = daysummary.no_of_discharge_cases
    result["no_of_probable_cases"] = daysummary.no_of_probable_cases
    result["no_of_hospitalised_cases_in_critical_condition"] = daysummary.no_of_hospitalised_cases_in_critical_condition

    d_14 = daysummary.as_of_date - timedelta(days=14)
    records = db.session.query(Case.report_date, func.count(Case.report_date).label('count')).filter(Case.report_date.between(d_14, daysummary.as_of_date)).group_by(Case.report_date).order_by(Case.report_date.desc())
    i = 0
    for record in records:
        if i == 0:
            result["no_of_confirmed_cases_today"] = record.count
        else:
            result["no_of_confirmed_cases_b"+str(i)] = record.count
        i+=1
            
    return result


def get_summary_for_past_14_from_db(): 
    d_14 = datetime.today() - timedelta(days=14)
    d_14 = d_14.replace(hour=0, minute=0, second=0, microsecond=0)
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    daysummarys = DaySummary.query.filter(DaySummary.as_of_date <= today).filter(DaySummary.as_of_date >= d_14).order_by(DaySummary.as_of_date)
    result = []
    for daysummary in daysummarys:
        o = {}
        o["as_of_date"] = daysummary.as_of_date.strftime("%d/%m/%Y")
        o["no_of_confirmed_cases"] = daysummary.no_of_confirmed_cases
        o["no_of_ruled_out_cases"] = daysummary.no_of_ruled_out_cases
        o["no_of_cases_still_hospitalised_for_investigation"] = daysummary.no_of_cases_still_hospitalised_for_investigation
        o["no_of_cases_fulfilling_the_reporting_criteria"] = daysummary.no_of_cases_fulfilling_the_reporting_criteria
        o["no_of_death_cases"] = daysummary.no_of_death_cases
        o["no_of_discharge_cases"] = daysummary.no_of_discharge_cases
        o["no_of_probable_cases"] = daysummary.no_of_probable_cases
        o["no_of_hospitalised_cases_in_critical_condition"] = daysummary.no_of_hospitalised_cases_in_critical_condition
        result.append(o) 
    return result
