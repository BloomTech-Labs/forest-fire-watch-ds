"""
Module to pull fire data from the MODUS project for use in BURN NOTICE
"""

#Imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
import time, schedule

# data source
# https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms
# website home for modis and viirs data


modis_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv'


def pull_modus(url = modis_url):
    """
    Get's modus data.
    """
    df = pd.read_csv(modis_url, sep=',')

    return df
    

def main():
    """
    Main function of python module. Calls pull_modus every hour and compares results to existing dataframe.
    """
    new_df = schedule.every().hour.do(pull_modus())

# TODO actually make this work



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

def check_fires(user_coords, fire_cords, perimiter=50):
    """
    checks a single user long/lat tuple against an array of long/lat fire coordinates
    and returns a dict of fires within the perimiter and a binary Alert: yes/no
    """
    
    results = {
        'Alert' : False,
        'Fires' : []
    }
    
    #iterate through the fire cord pairs
    for cord in fire_cords:
        
        #compare user_coords with individual fires
        distance = haversine(user_coords[0], user_coords[1], cord[0], cord[1])

        # if this fire is on or within the user perimiter we set the alert flag and save the fire data
        if distance <= perimiter:
            results['Alert'] = True
            
            fire_location_tuple = ((cord[0], cord[1]), distance)
            #the fire location tuples will have the form

            # list of ([long, lat], distance_to_user)
            results['Fires'].append(fire_location_tuple)
        
        else:
            pass
    
    return results

# Start process
if __name__ == '__main__':
    main()