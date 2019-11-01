"""
Functions to get fires from Inciweb and check distance between users and fires.
"""

########################################################
######################## Imports #######################
########################################################

# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

# Other imports
import feedparser
import re


#######################################################
####################### Functions #####################
#######################################################

# Function to pull all fires
def fires_list():
    url = 'https://inciweb.nwcg.gov/feeds/rss/incidents/'
    fires = feedparser.parse(url)
    rss_fires = []
    for entry in fires.entries:
    # Return a dict for each fire with name and location
        fire_dict = {'name': entry.title, 'location': entry.where.coordinates}
        rss_fires.append(fire_dict)
    return rss_fires

# Fires list with type 
def fires_list_type():
    url = 'https://inciweb.nwcg.gov/feeds/rss/incidents/'
    fires = feedparser.parse(url)
    rss_fires = []
    for entry in fires.entries:
    # Return a dict for each fire with name, location, and type
        # Get the type of fire
        if 'wildfire' in entry.title.lower():
            fire_type = 'Wildfire'
        elif 'prescribed' in entry.title.lower():
            fire_type = 'Prescribed Fire'
        elif 'burned area emergency response' in entry.title.lower():
            fire_type = 'Burned Area Emergency Response'
        else:
            fire_type = 'NA'

        name = re.sub("[\(\[].*?[\)\]]", "", entry.title).replace('Prescribed Fire', '').replace('Prescribed Burn', '').replace('BAER', '') # Remove from entry.title


        fire_dict = {'name': name, 'location': entry.where.coordinates, 'type': fire_type}
        rss_fires.append(fire_dict)
    return rss_fires

# Distance function
def haversine(lon1, lat1, lon2, lat2):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 3956  # radius of earth in miles mean of  poles and equator radius
    return c * r

# Sort fires by distance - import the JSON from web
def sort_fires(values):

    # json type for post:
    # {
    #     position: [lat, lon],
    #     radius: int
    # }

    # Get args for Haversine
    lat1, lon1 = values['position'][0], values['position'][1]
    radius = values['radius']

    # Initialize fire lists
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

    return nearby_fires, other_fires