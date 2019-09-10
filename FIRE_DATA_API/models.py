"""
SQLAlchemy models for TwitOff.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Modus(db.Model):
    """Twitter users that we pull and analyze Tweets for."""
    id = db.Column(db.BigInteger, primary_key=True)
    latitude = db.Column(db.NUMERIC(6,3))
    longitude = db.Column(db.NUMERIC(6,3))
    brightness = db.Column(db.FLOAT(2))
    scan = db.Column(db.FLOAT(1))
    # track = 
    # acq_date =
    # acq_time = 
    # satellite = 
    # confidence = 
    # bright_t31 = 
    # frp = 
    # daynight = 

    def __repr__(self):
        return "<lat/long {},{}>".format(self.latitude, self.longitude)


