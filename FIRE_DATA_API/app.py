"""
Module to pull fire data from the MODUS project for use in Fire Flight.

User can send coordinates to API along with a perimiter value (in miles) and receive
an alert if there are active fires within that perimter.
"""

# Flask App Imports
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS #, cross_origin
from json import dumps

# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from pandas.util.testing import assert_frame_equal

# Different schedulers for querying data
from apscheduler.schedulers.background import BackgroundScheduler
# import schedule, time


# data source
# https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms
# website home for modis and viirs data

# define flask app and api
app = Flask(__name__)
# enable CORS on all app routes
CORS(app)
api = Api(app)



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
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 3956 #radius of earth in miles mean of  poles and equator radius
        return c * r

def check_fires(user_coords, perimiter, fire_coords):
    """
    checks a single user long/lat tuple against an array of long/lat fire coordinates
    and returns a dict of fires within the perimiter and a binary Alert: yes/no
    """

    results = {
        'Alert' : False,
        'Fires' : []
    }
    
    #iterate through the fire coord pairs
    for coord in fire_coords:
        
        #compare user_coords with individual fires
        distance = haversine(user_coords[0], user_coords[1], coord[0], coord[1])

        # if this fire is on or within the user perimiter we set the alert flag and save the fire data
        if distance <= perimiter:
            results['Alert'] = True
            
            fire_location_tuple = ((coord[0], coord[1]), distance)
            #the fire location tuples will have the form

            # list of ([long, lat], distance_to_user)
            results['Fires'].append(fire_location_tuple)
        
        else:
            pass
    
    return results

class CheckFires(Resource):
    """
    Get's User long/lat coordinates and returns a json
    """

    def post(self):
        values = request.get_json()

        user_coords = values['user_coords'] #I want to get a json like:
        #{'user_coords' : (long, lat), 'distance': number} 
        try:
            perimiter = values['distance']
        except:
            perimiter = 50

        #get's all high confidence fire coords from our df
        fire_coords = df.loc[df['confidence'] > 90][['longitude', 'latitude']].values

        return jsonify(check_fires(user_coords, perimiter, fire_coords))

class AllFires(Resource):
    """
    Returns a json with all active fires
    """

    def get(self):
        
        #get all fire coords
        fire_coords = df.loc[df['confidence'] > 90][['longitude', 'latitude']].values

        results = {
            'Alert' : True,
            'Fires' : [tuple(x) for x in fire_coords]
        }

        return jsonify(results)

# connects resources to api endpoint
api.add_resource(CheckFires, "/check_fires")
api.add_resource(AllFires, "/all_fires")


modis_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv'

def pull_modus(url = modis_url):
    """
    Get's modus data.
    """
    df = pd.read_csv(url, sep=',')

    return df

#defines our first df from memory
# df = pd.read_csv('modus_df', sep=',')
df = pull_modus()
    
def check_new_df():
    """
    Pulls a new df from modus and compares it to the live df
    """
    new_df = pull_modus()

    #compares new_df to existing df, if equal it passes
    try:
        if assert_frame_equal(df, new_df):
            pass
        else:
            pass

    except:
        df = new_df.copy()
        return df        
    
# pulls a new df every hour
scheduler = BackgroundScheduler()
scheduler.add_job(check_new_df, 'interval', hours=1)
scheduler.start()

# manually update csv
@app.route('/data/update', methods=['GET'])
def check_modus_data():
    new_df = check_new_df()
    size = new_df.shape
    global df
    df = new_df

    return jsonify({'new df size ': size}), 201

# check our df size
@app.route('/data/size', methods=['GET'])
def df_size():
    size = df.shape
    return jsonify({'df_size' : size}), 201

# check our df head
@app.route('/data/head', methods=['GET'])
def df_head():
    head = df.head().to_json()
    return jsonify({'df_head' : head}), 201

# Start process
if __name__ == '__main__':
    app.run()