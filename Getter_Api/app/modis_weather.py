from functions import (
    get_weather, get_modis_data, reduce_points, 
    add_weather_columns, populate_weather, label_fires,
    process_live_data, clean_df
    )
import time
import psycopg2
import urllib.parse as up
import datetime
import os

import feedparser

# Get the database url from environment variables
db_url = os.environ.get('DB_URL')

# Get the modis data
df = get_modis_data()
df = process_live_data(df)

# Reduce number of points
df = reduce_points(df)

# Add empty weather columns
df = add_weather_columns(df)

# Populate the df with the weather
populate_weather(df)

# Add timestamp
insert_time = str(datetime.datetime.now())
df['timestamp'] = [insert_time for i in range(len(df['week']))]

# Label the data
df = label_fires(df)

# get rid of nan values
df = clean_df(df)

# Credentials
dbname = 'iagqhysc'
user = 'iagqhysc'
password = '' # Don't commit this!
host = 'salt.db.elephantsql.com'

# Establish connection
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                       password=password, host=host)

# Instantiate cursor
pg_curs = pg_conn.cursor()

# Send data to db
print('cleaning data')
dirty_rows = df.values

# Clean up rows
rows = []

for row in dirty_rows:
    rows.append(tuple(row))

print('adding data to DB')
# Loop over the array to write rows in the DB
for row in rows:
    print(len(row))
    insert = """
    INSERT INTO training
    (latitude, longitude, brightness, scan, track,
     satellite, confidence, version, bright_t31, frp,
     daynight, month, week, temperature, humidity, windspeed,
     winddirection, timestamp, fire)
    VALUES 
    """ + str(row) + ';'
    
    pg_curs.execute(insert)

# Save and finish session
pg_curs.close()
pg_conn.commit()

print('all done!')
