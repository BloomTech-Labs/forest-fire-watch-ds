from functions import get_weather, get_modis_data, reduce_points, add_weather_columns, populate_weather
import time

# Get the modis data
df = get_modis_data()

# Reduce number of points
df = reduce_points(df)

# Add empty weather columns
df = add_weather_columns(df)

# Populate the df with the weather
populate_weather(df)

##### NEXT UP: ADD DF TO DATABASE #####