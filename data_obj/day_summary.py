from db import db

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

