from db import db
from datetime import datetime

class DaySummary(db.Model):
    __tablename__ = 'DaySummary'
    as_of_date = db.Column(db.DateTime, primary_key=True)
    no_of_confirmed_cases = db.Column(db.Integer)
    no_of_ruled_out_cases = db.Column(db.Integer)
    no_of_cases_still_hospitalised_for_investigation = db.Column(db.Integer)
    no_of_cases_fulfilling_the_reporting_criteria = db.Column(db.Integer)
    no_of_death_cases = db.Column(db.Integer)
    no_of_discharge_cases = db.Column(db.Integer)
    no_of_probable_cases = db.Column(db.Integer)
    no_of_hospitalised_cases_in_critical_condition = db.Column(db.Integer)


    def __repr__(self):
        return '<Case Summary %exir>' %self.as_of_date
    

    def __to_dictionary__(self):
        o = {}
        o["as_of_date"] = self.as_of_date.strftime("%d/%m/%Y")
        o["no_of_confirmed_cases"] = self.no_of_confirmed_cases
        o["no_of_ruled_out_cases"] = self.no_of_ruled_out_cases
        o["no_of_cases_still_hospitalised_for_investigation"] = self.no_of_cases_still_hospitalised_for_investigation
        o["no_of_cases_fulfilling_the_reporting_criteria"] = self.no_of_cases_fulfilling_the_reporting_criteria
        o["no_of_death_cases"] = self.no_of_death_cases
        o["no_of_discharge_cases"] = self.no_of_discharge_cases
        o["no_of_probable_cases"] = self.no_of_probable_cases
        o["no_of_hospitalised_cases_in_critical_condition"] = self.no_of_hospitalised_cases_in_critical_condition
        return o

