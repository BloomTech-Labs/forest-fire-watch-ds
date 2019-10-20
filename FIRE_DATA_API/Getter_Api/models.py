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

class Weather_Curr(db.Model):
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



        

