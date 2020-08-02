

def convert_building_name_to_geo(building_name):
    return building_name.upper().replace("(NON-RESIDENTIAL)", "").strip()