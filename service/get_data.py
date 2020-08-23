import json
import math
from data_obj.case import *
from data_obj.day_summary import *
from data_obj.related_building import *
from data_obj.building_geo import *
from datetime import datetime, timedelta
from db import db
from sqlalchemy import *
from util.utils import convert_building_name_to_geo


def get_case_no_of_page(record_per_page):
    rows = db.session.query(func.count(Case.case_no)).scalar()
    page = math. ceil(rows / record_per_page)
    return page


def get_case_by_page(page,record_per_page):
    start_record = page * record_per_page +1
    end_record = (page+1) * record_per_page
    count = 0
    cases = Case.query.order_by(Case.case_no.desc()).all()
    result = []
    for case in cases:
        count+=1
        if count >= start_record and count <=end_record:
            result.append(case.to_dictionary())
        elif count > end_record:
            break

    return result



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
    result = daysummary.to_dictionary()

    d_14 = daysummary.as_of_date - timedelta(days=14)
    records = db.session.query(Case.report_date, func.count(Case.report_date).label('count')).filter(Case.report_date.between(d_14, daysummary.as_of_date)).group_by(Case.report_date).order_by(Case.report_date.desc())
    i = 0
    max_case_no = 0
    for record in records:
        if i == 0:
            result["no_of_confirmed_cases_today"] = record.count
        else:
            result["no_of_confirmed_cases_b"+str(i)] = record.count
        i+=1
        if(record.count > max_case_no):
            max_case_no = record.count

    result["max_case_no"] = max_case_no
        

    return result


def get_summary_for_past_14_from_db(): 
    d_14 = datetime.today() - timedelta(days=14)
    d_14 = d_14.replace(hour=0, minute=0, second=0, microsecond=0)
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    daysummarys = DaySummary.query.filter(DaySummary.as_of_date <= today).filter(DaySummary.as_of_date >= d_14).order_by(DaySummary.as_of_date)
    result = []
    for daysummary in daysummarys:
        result.append(daysummary.to_dictionary()) 
    return result


def get_latest_related_building_from_db(): 
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    related_buildings = RelatedBuilding.query.filter(RelatedBuilding.as_of_date == today).order_by(RelatedBuilding.district)
    result = []
    for related_building in related_buildings:
        o = related_building.to_dictionary()

        trim_building_name = convert_building_name_to_geo(related_building.building_name)
        building_geo_from_db = BuildingGeoInfo.query.filter(BuildingGeoInfo.district == related_building.district).filter(BuildingGeoInfo.building_name == trim_building_name).first()
        if building_geo_from_db is not None:
            o["lat"] = building_geo_from_db.lat
            o["lon"] = building_geo_from_db.lon
        else:
            o["lat"] = "NULL"
            o["lon"] = "NULL"
        result.append(o) 
    return result

def get_latest_district_data_from_db():
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    districts = db.session.query(RelatedBuilding.district, func.sum(RelatedBuilding.no_of_case).label('no_of_case')).filter(RelatedBuilding.as_of_date == today).group_by(RelatedBuilding.district).order_by(RelatedBuilding.district)   
    result = []
    for district in districts:
        o = {}
        o["district"] = district.district
        o["no_of_case"] = district.no_of_case
        result.append(o) 
    return result


def get_building_geo_data_from_db():
    geo_data_arr = BuildingGeoInfo.query.order_by(BuildingGeoInfo.district).all()
    result = []
    for geo_data in geo_data_arr:
        result.append(geo_data.to_dictionary()) 
    return result

def get_building_without_geo_data_from_db():
    related_buildings = RelatedBuilding.query.filter(
        ~BuildingGeoInfo.query
        .filter(BuildingGeoInfo.district == RelatedBuilding.district)
        .filter(func.trim(func.replace(func.upper(BuildingGeoInfo.building_name),'(NON-RESIDENTIAL)','')) == func.trim(func.replace(func.upper(RelatedBuilding.building_name),'(NON-RESIDENTIAL)','')))
        .exists()
    ).order_by(RelatedBuilding.district).all()
    result = []
    dis_building_dic = {}
    for related_building in related_buildings:
        trim_building_name = convert_building_name_to_geo(related_building.building_name)
        building_geo_from_db = BuildingGeoInfo.query.filter(BuildingGeoInfo.district == related_building.district).filter(BuildingGeoInfo.building_name == trim_building_name).first()
        if building_geo_from_db is None:
            key = related_building.district+"_"+trim_building_name
            if key not in dis_building_dic.keys():
                dis_building_dic[key] = "Y"
                o = {}
                o["district"] = related_building.district
                o["building_name"] = trim_building_name
                result.append(o) 
    return result
