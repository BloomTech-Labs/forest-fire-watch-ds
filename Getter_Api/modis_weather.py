from functions import get_weather, get_modis_data, reduce_points, add_weather_columns, populate_weather
import time
import psycopg2
import urllib.parse as up
import datetime
import os

# Get the database url from environment variables
db_url = os.environ.get('DB_URL')

# Get the modis data
df = get_modis_data()

# Reduce number of points
df = reduce_points(df)

# Add empty weather columns
df = add_weather_columns(df)

# Populate the df with the weather
populate_weather(df)

# Connect to database and insert values
up.uses_netloc.append('postgres')
url = up.urlparse(db_url)
insert_time = datetime.datetime.now()
for i in df.values:
  query = '''
  INSERT INTO modis_weather VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
  '''
  with psycopg2.connect(database=url.path[1:],
                        user=url.username,
                        password=url.password,
                        host=url.hostname,
                        port=url.port) as conn:
    with conn.cursor() as curs:
      curs.execute(query, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8],
                           i[9], i[10], i[11], i[12], i[13], i[14], i[15],
                           i[16], insert_time))

