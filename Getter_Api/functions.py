# System Imports
import os
import requests
import json 

# API Tokens 
nasa_lance_token = ''
open_weather_token = ''

# DB Imports
from .models import Modis, db

# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
import json
import config

# Functions 

# MODIS Functions
def pull_modis():
    """
    Get latest modis data.
    """
    print("pulling modus - sleep for 1")
    time.sleep(1)

    url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv"
    df = pd.read_csv(url, sep=",")
    print("got dataframe ", df.shape)
    return df

def process_live_data(original_df):
    """
    Pre processes live data to match pipeline expectations.
    """
    print("process_live_data!")
    df = original_df.copy()
    # process satellite labels
    df["satellite"] = df["satellite"].replace({"T": "Terra", "A": "Aqua"})

    # process time features
    df["acq_time"] = (df["acq_time"] // 100) * 60 + (df["acq_time"] % 100)
    df["timestamp"] = df.apply(
        lambda x: datetime.datetime.strptime(x["acq_date"], "%Y-%m-%d")
        + datetime.timedelta(minutes=x["acq_time"]),
        axis=1,
    )
    df["month"] = df["timestamp"].dt.month
    df["week"] = df["timestamp"].dt.weekofyear
    df.drop(columns=["acq_date", "acq_time"], inplace=True)

    return df

def add_training_data(df, db):
    print('adding training data')

    # Add data from df into array
    for row in df.values:
        data = Modis(
            latitude = row[0],
            longitude = row[1],
            brightness = row[2],
            scan = row[3],
            track = row[4],
            satellite = row[5],
            confidence = row[6],
            version = row[7],
            bright_t31 = row[8],
            frp = row[9],
            daynight = row[10],
            timestamp = row[11],
            month = row[12],
            week = row[13]
        )

        # add to db
        db.session.add(data)

    # commit
    db.session.commit()
    

def get_lon():
    pass

def get_lat():
    pass

def get_firms():
    lance_firms_url = 'https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS'
    lance_firms_wget = f'wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 "{lance_firms_url}" --header "Authorization: Bearer {config.nasa_lance_token}" -P ../../'
    return os.system(lance_firms_wget)

def get_weather(lat, lon):
    open_weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={config.weather_key}'
    response = requests.get(open_weather_url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return response.status_code
    
    
# prob need a function to check if  user input is within an already checked radius
# so as not to exceed request limit of Open weather data.
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


## Notes 

# open weather has a retangular box api call that may solve this problem 