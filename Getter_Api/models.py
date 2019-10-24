from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Modis(db.Model): 
    """ Modis Observation"""
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    brightness = db.Column(db.Float)
    scan = db.Column(db.Float)
    track = db.Column(db.Float)
    satellite = db.Column(db.VARCHAR(7))
    confidence = db.Column(db.Integer)
    version = db.Column(db.VARCHAR(7))
    bright_t31 = db.Column(db.Float)
    frp = db.Column(db.Float)
    daynight = db.Column(db.VARCHAR(7))
    timestamp = db.Column(db.DateTime, index=True)
    month = db.Column(db.Integer)
    week = db.Column(db.Integer)

    def __repr__(self):
        return """<lat/long/brightness/scan/track/satellite/confidence/
        version/bright_t31/frp/daynight/timestamp/month/week {}, {}, {}, 
        {}, {}, {}, {}, {}, {}, {}, {}, {} 
        {}, {}>""".format(self.latitude, self.longitude, 
        self.fire, self.timest)

""" class Weather_Curr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.VARCHAR(7))
    longitude = db.Column(db.VARCHAR(7))
    wind_speed = db.Column()
    wind_deg = db.Column()
    clouds = db.Column()
    rain_1h = db.Column()
    rain_3h = db.Column()
    snow_1h = db.Column()
    snow_3h = db.Column()

    def __repr__(self):
        return ("<lat/long/wind_speed/wind_deg/clouds/rain_1h/rain_3h/snow_1h/snow_3h {}, {}, {} {}, {}, {}, {}, {}, {}>".format(
            self.latitude, self.longitude, self.timestamp self.wind_speed, self.wind_deg, 
            self.clouds, self.rain_1h, self.rain_3h, self.snow_1h, self.snow_3h ))

class FIRMS(db.Model): 
    def __repr__(self):
        return("< {}>".format(self)) """