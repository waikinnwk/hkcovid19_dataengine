from db import db

class BuildingGeoInfo(db.Model):
    __tablename__ = 'BuildingGeoInfo'
    district = db.Column(db.String(50), primary_key=True)
    building_name = db.Column(db.String(200), primary_key=True)
    lat = db.Column(db.String(200))
    lon = db.Column(db.String(200))



    def __repr__(self):
        return '<BuildingGeoInfo %exir>' %self.building_name

    
    def to_dictionary(self):
        o = {}
        o["district"] = self.district
        o["building_name"] = self.building_name
        o["lat"] = self.lat
        o["lon"] = self.lon
        return o