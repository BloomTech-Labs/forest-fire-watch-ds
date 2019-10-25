"""
Functions to check distance between users and fires.
"""

# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt


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


def check_fires(user_coords, perimiter, fire_coords):
    """
    checks a single user long/lat tuple against an array of long/lat fire coordinates
    and returns a dict of fires within the perimiter and a binary Alert: yes/no
    """

    results = {"Alert": False, "Fires": []}

    # iterate through the fire coord pairs
    for coord in fire_coords:

        # compare user_coords with individual fires
        distance = haversine(user_coords[0], user_coords[1], coord[0], coord[1])

        # if this fire is on or within the user perimiter we set the alert flag and save the fire data
        if distance <= perimiter:
            results["Alert"] = True

            fire_location_tuple = ((coord[0], coord[1]), distance)
            # the fire location tuples will have the form

            # list of ([long, lat], distance_to_user)
            results["Fires"].append(fire_location_tuple)

        else:
            pass

    return results
