from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Active_Fire(db.Model): 
    """ Modis Observation"""
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.VARCHAR(7))
    longitude = db.Column(db.VARCHAR(7))
    fire = db.Column(db.SmallInteger)
    timestamp = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return "<lat/long/fire/timestamp {},{}, {}, {}>".format(self.latitude, self.longitude, 
        self.fire, self.timest)