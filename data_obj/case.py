from db import db

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
