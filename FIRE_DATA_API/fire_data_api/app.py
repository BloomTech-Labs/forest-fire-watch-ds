"""
Module to pull fire data from the MODUS project for use in Fire Flight.

User can send coordinates to API along with a perimiter value (in miles) and receive
an alert if there are active fires within that perimter.
"""

# Flask App Imports
from flask import Flask, jsonify, request, json
from flask_restful import Api, reqparse
from flask_cors import CORS



# local imports
from .models import db, Fire, FrameHash
from .resources import CheckFires, AllFires
from .functions import haversine
from .datascience import (
    check_new_df,
    process_live_data,
    classify_fires,
    add_fires,
    check_model
)

from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import os
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import feedparser


def fires_list():
    url = 'https://inciweb.nwcg.gov/feeds/rss/incidents/'
    fires = feedparser.parse(url)
    rss_fires = []
    for entry in fires.entries:
    # Return a dict for each fire with name and location
        fire_dict = {'name': entry.title, 'location': entry.where.coordinates}
        rss_fires.append(fire_dict)
    return rss_fires


def create_app():
    """
    Creates and configures an instance of our Flask API
    """
    app = Flask(__name__)
    # create db first

    # configure database variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["ENV"] = os.environ.get(
        "ENV"
    )  # apparently this doesn't really work so commenting out for now

    app.app_context().push()
    db.init_app(app)

    # enable CORS on all app routes
    CORS(app)

    # initialize the api wrapper
    api = Api(app)
    

    # grab all RSS fires
    @app.route("/rss_fires", methods=["GET"])
    def rss_fires():
        # Open RSS page and parse lxml
        lxml = urlopen('https://inciweb.nwcg.gov/feeds/rss/incidents/')
        soup = BeautifulSoup(lxml, 'lxml')
        # Retrieve by tag
        dirty_lats = soup.find_all('geo:lat')
        dirty_lons = soup.find_all('geo:long')

        # Clean the tags out
        lats = []

        for dirty_lat in dirty_lats:
            exp = re.compile('[0-9]+.[0-9]+')
            lats.append(float(re.findall(exp, str(dirty_lat))[0]))
            

        lons = []

        for dirty_lon in dirty_lons:
            exp = re.compile('[0-9]+.[0-9]+')
            lons.append(float(re.findall(exp, str(dirty_lon))[0]))

        # instantiate location list
        location_list = []

        # iterate
        for i in range(len(lats)):
            loc = (lats[i], lons[i])
            
            location_list.append(loc)

        # Return
        return location_list


    # grab RSS fires using feedparser
    @app.route("/fpfire", methods=["GET"])
    def fires_json():
        rss_fires = fires_list()
        return jsonify(rss_fires)

    
    @app.route("/check_rss_fires", methods=["POST"])
    def check_rss_fires(): # (lat, lon)
        values = request.get_json()

        # json type for post
        # {
        #     position: [lat, lon],
        #     radius: int
        # }

        # Get args for Haversine
        lat1, lon1 = values['position'][0], values['position'][1]
        radius = values['radius']
        
        # Initialize nearby fires
        nearby_fires = []
        other_fires = []
        
        # get list of all fires
        fires = fires_list()

        # iterate through fires
        for fire in fires:
            dist = haversine(lon1, lat1, fire['location'][0], fire['location'][1]) # haversine(lon1, lat1, lon2, lat2)
            if dist <= radius:
                nearby_fires.append(fire)
            else:
                other_fires.append(fire)
        
        return jsonify({'nearby_fires': nearby_fires, 'other_fires': other_fires})

    return app
