# System Imports
import os
import requests
import json 
import time
import datetime

# API Tokens 
# Add api keys to Heroku config vars to access them
# Using Openweather API
open_weather_token = os.environ.get('WEATHER_KEY')

# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
import feedparser

# Functions 

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

def get_weather(lat, lon):
    open_weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&APPID={open_weather_token}'
    response = requests.get(open_weather_url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return response.status_code
    
def get_modis_data():
    modis_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv"
    modis_data = pd.read_csv(modis_url)
    return modis_data

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
    # df['version'] = df['version'].apply(str)
    df["month"] = df["timestamp"].dt.month
    df["week"] = df["timestamp"].dt.weekofyear
    df.drop(columns=["acq_date", "acq_time", "timestamp"], inplace=True)

    return df

# Getting the centermost point of a cluster
def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)

# Reduces the number of points in the modis data frame
def reduce_points(df, distance = 1.5):
    # Rename the latitude and longitude columns for ease
    df = df.rename({'latitude': 'lat', 'longitude': 'lon'}, axis=1)

    # Get the data points where the confidence is above 70
    df = df[df['confidence'] >= 70]

    # Grab the coords of the df
    coords = df.as_matrix(columns=['lat', 'lon'])

    # Compute DBSCAN; distance is the max distance for 'cluster'
    kms_per_radian = 6371.0088
    epsilon = distance / kms_per_radian

    # use the haversine metric and ball tree algorithm to calculate great circle distances between points
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])

    # returns the center-most point from a cluster
    centermost_points = clusters.map(get_centermost_point)

    # turn these center-most points into a pandas dataframe
    lats, lons = zip(*centermost_points)
    rep_points = pd.DataFrame({'lon':lons, 'lat':lats})

    # pull the full row from the original data set where the lat and lon match
    rs = rep_points.apply(lambda row: df[(df['lat']==row['lat']) & (df['lon']==row['lon'])].iloc[0], axis=1)
    
    return rs

# Adds the empty weather columns
def add_weather_columns(df):
    df['temp'] = np.nan
    df['humidity'] = np.nan
    df['wind_speed'] = np.nan
    df['wind_direction'] = np.nan

    return df

# Adds weather to modis dataframe
def populate_weather(df):
  api_count = 0
  for i in range(df.shape[0]):
    if api_count % 60 != 0:
      lat = df.lat[i]
      lon = df.lon[i]
      weather = get_weather(lat, lon)
      api_count += 1
      df['temp'][i] = weather['main']['temp']
      df['humidity'][i] = weather['main']['humidity']
      df['wind_speed'][i] = weather['wind']['speed']
      if 'deg' in weather['wind']:
        df['wind_direction'][i] = weather['wind']['deg']

    elif api_count == 0:
      lat = df.lat[i]
      lon = df.lon[i]
      weather = get_weather(lat, lon)
      api_count += 1
      df['temp'][i] = weather['main']['temp']
      df['humidity'][i] = weather['main']['humidity']
      df['wind_speed'][i] = weather['wind']['speed']
      if 'deg' in weather['wind']:
        df['wind_direction'][i] = weather['wind']['deg']

    else:
      print('Sleeping for 60 seconds')
      time.sleep(60)
      print('Starting up again')
      lat = df.lat[i]
      lon = df.lon[i]
      weather = get_weather(lat, lon)
      api_count += 1
      df['temp'][i] = weather['main']['temp']
      df['humidity'][i] = weather['main']['humidity']
      df['wind_speed'][i] = weather['wind']['speed']
      if 'deg' in weather['wind']:
        df['wind_direction'][i] = weather['wind']['deg']
  
  return 'Done'

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

# Label data
def label_fires(df):
    print('labelling data')
    # Instantiate labels list
    labels = []
    
    # Get lats and lons from df
    lats = df['lat'].tolist()
    lons = df['lon'].tolist()
    
    # Pull confirmed fires
    fires = fires_list()
    locations = [entry['location'] for entry in fires]
    
    # loop data points
    for n in range(len(lats)):
        # loop fires
        for fire in locations:
            distance = haversine(lons[n], lats[n], fire[1], fire[0])
            label = 0
            if distance < 0.3:
                label = 1
                labels.append(label)
                break
            else:
                pass

        if label != 1:
            labels.append(label)
            
    # append labels to df
    labelled_df = df.copy()
    labelled_df['fire'] = labels
    
    return labelled_df

def clean_df(df):
    clean_df = df.fillna(0)
    return clean_df