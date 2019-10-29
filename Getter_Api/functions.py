# System Imports
import os
import requests
import json 
import time

# API Tokens 
nasa_lance_token = os.environ.get('NASA_LANCE_TOKEN')
open_weather_token = os.environ.get('WEATHER_KEY')

# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

# Functions 

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
    lance_firms_wget = f'wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 "{lance_firms_url}" --header "Authorization: Bearer {nasa_lance_token}" -P ../../'
    return os.system(lance_firms_wget)

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