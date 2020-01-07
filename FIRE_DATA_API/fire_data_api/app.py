"""
Heroku App to pull current fire alerts from Inciweb for use in Wildfire Watch App.

User can send coordinates to API along with a radius value (in miles) and receive
an alert if there are active fires within that radius.
"""


#############################################
################ Imports ####################
#############################################

# Flask App Imports
from flask import Flask, jsonify, request, json
from flask_restful import Api, reqparse
from flask_cors import CORS
import requests

# local imports
from .functions import fires_list, haversine, sort_fires, fires_list_type
from .functions import get_aqi_data,get_nearest_stations


# Other imports
import datetime
import os
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import feedparser


###########################################
############# Create App ##################
###########################################

def create_app():
    """
    Creates and configures an instance of our Flask API
    """
    app = Flask(__name__)

    # enable CORS on all app routes
    CORS(app)

    # initialize the api wrapper
    api = Api(app)
    

    ############################################################
    ################### ENDPOINTS / ROUTES #####################
    ############################################################

    # grab RSS fires using feedparser (YOU NEED CHANCE'S VERSION)
    @app.route("/fpfire", methods=["GET"])
    def fires_json():
        rss_fires = fires_list()
        return jsonify(rss_fires)


    @app.route("/fpfiretype", methods=["GET"])
    def firestype_json():
        rss_fires = fires_list_type()
        return jsonify(rss_fires)


    # Return list of nearby_fires and other_fires
    @app.route("/check_rss_fires", methods=["POST"])
    def check_rss_fires(): # (lat, lon)
        values = request.get_json()

        # json type for post
        # {
        #     position: [lat, lon],
        #     radius: int
        # }

        # Sort fires using sort_fires function
        nearby_fires, other_fires = sort_fires(values)
        
        return jsonify({'nearby_fires': nearby_fires, 'other_fires': other_fires})


    # grab RSS fires using BeautifulSoup (IF YOU DON'T HAVE CHANCE'S VERSION)
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
        return jsonify({'location': location_list})

    #Get the Air Quality data from the nearest station for the given lat,long
    @app.route("/get_aqi_data",methods=['GET'])
    def aqi_data():
        # print(request)
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        aqi_data = get_aqi_data(lat,lng)
        return jsonify(aqi_data)

    #Find the Latitude and longitude of nearest weather stations
    @app.route("/get_aqi_stations",methods=['GET'])
    def aqi_stations():
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        distance = request.args.get('distance')
        #Convert the parameters into float for further operations
        try:
            stations_data = get_nearest_stations(float(lat),float(lng),float(distance))
            return jsonify(stations_data)
        except:
            return "error:bad parameters"


    # Close up the create_app() function
    return app