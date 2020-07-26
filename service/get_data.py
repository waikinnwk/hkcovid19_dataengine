from data_obj.case import *


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