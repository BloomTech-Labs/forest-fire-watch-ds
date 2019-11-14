# Getting the app up and running

## Setting up Heroku apps
For Heroku, we had two separate apps one that was used for the RSS feed endpoint for the front-end, and another one that was used for gathering data and putting it into a postgreSQL (elephant SQL in this case)

### Getting the main app setup
- Create Heroku app
- When deploying the main wildfirewatch app, do it from within `FIRE_DATA_API` folder

### Getting the Getter app setup (this one is more in-depth)
1. Create the Heroku app
2. Create your config variables:
	-- One will be the weather api key from [OpenWeather](https://openweathermap.org/api) make sure you name it `WEATHER_KEY`
	-- The other config var will be `DB_URL` which is the url for the elephantSQL database that we are storing data, we will probably end up giving you guys the database that's already up so that you don't have to make a new one and migrate all of the data.
3. Next you've got to set up a scheduler on Heroku  that run the `modis_weather.py` file once every 24 hours
	-- You can find the scheduler I used under the resources tab in Heroku, it's called `Heroku Scheduler`. However you have to have payment type on file in order to use it. I just used my own CC, but I heard you can use other payment types to get around this. (i.e. An expired PayPal card, maybe a gift card visa will work too.)
4. You should be ready to deploy the Getter App to Heroku now. Do this from within the `Getter_Api` folder.


## What are the functions?

### FIRE_DATA_API functions
- `fires_list()`
	- Returns all of the fires from the RSS feed
- `fires_list_type()`
	- Returns all of the fires from the RSS feed with the type of fires seperate from the name
- `geopy.great_circle((lat0, lon0), (lat1, lon1)).miles`
	- Returns the distance in miles between two sets of points
- `sort_fires(values)`
	-  Returns fires that are in range of values and also returns the one that are not. (Values = lat, lon, radius)

### Getter_Api functions
- `get_weather(lat, lon)`
	- Returns the weather from the OpenWeather API at a given lat, lon
- `get_modis_data()`
	- Returns a data frame of the current MODIS data
- `process_live_data(original_df)`
	- Returns a processed data frame of the MODIS data
- `get_centermost_point(cluster)`
	- Returns the centermost point in a cluster (used in `reduce_points()` function) 
- `reduce_points(df, distance = 1.5)`
	- Returns a data frame of the modis data but with reduced points (clusters them together and find the centermost points)
- `add_weather_columns(df)`
	- Returns a df with weather columns added to it
- `populate_weather(df)`
	- Returns a df with the weather columns populated
	- Takes time so the api doesn't time out (60 calls per second)
	- May have NaN's in the `wind_direction` column
- `label_fires(df)`
	- Returns a df of the modis data with labels of whether or not it's a fire
- `clean_df(df)`
	- returns df with NaN's filled with `0`
	- Pretty much for the wind direction
