from db import db

class RelatedBuilding(db.Model):
    __tablename__ = 'RelatedBuilding'
    as_of_date = db.Column(db.DateTime, primary_key=True)
    district = db.Column(db.String(50))
    building_name = db.Column(db.String(200), primary_key=True)
    last_date_of_residence_of_the_case = db.Column(db.String(50))
    related_case = db.Column(db.String(500))
    no_of_case = db.Column(db.Integer)


    def __repr__(self):
        return '<Related Building %exir>' %self.building_name
