"""
SQLAlchemy models for FireWatch.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Fire(db.Model):
    """Modis observations that we have classified."""
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.VARCHAR(7))
    longitude = db.Column(db.VARCHAR(7))
    fire = db.Column(db.SmallInteger)
    timestamp = db.Column(db.DateTime, index=True)
    

    def __repr__(self):
        return "<lat/long/fire/timestamp {},{}, {}, {}>".format(self.latitude, 
        self.longitude, self.fire, self.timestamp)

class FrameHash(db.Model):
    """
    A table of df hashes from modis. Allows us to check if dfs have already been added
    to our Fire database.  
    """
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.VARCHAR(50))
    timestamp = db.Column(db.DateTime, index=True)


    def __repr__(self):
        return "<hash/timestamp{},{}>".format(self.hash, self.timestamp)

