from db import db
from datetime import datetime

class Case(db.Model):
    __tablename__ = 'Case'
    case_no = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.DateTime)
    onset_date = db.Column(db.String(50))
    gender =  db.Column(db.String(8))
    age = db.Column(db.Integer)
    admitted_hospital =  db.Column(db.String(200))
    hospital_status =  db.Column(db.String(50))
    is_hk_resident =  db.Column(db.String(50))
    case_classification = db.Column(db.String(300))
    status =  db.Column(db.String(50))
    def __repr__(self):
        return '<Case %exir>' %self.id

    def to_dictionary(self):
        o = {}
        o["case_no"] = self.case_no
        o["report_date"] = self.report_date.strftime("%d/%m/%Y")
        o["onset_date"] = self.onset_date
        o["gender"] = self.gender
        o["age"] = self.age
        o["admitted_hospital"] = self.admitted_hospital
        o["hospital_status"] = self.hospital_status
        o["is_hk_resident"] = self.is_hk_resident
        o["case_classification"] = self.case_classification
        o["status"] = self.status    
        return o   
