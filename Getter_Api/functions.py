
# System Imports
import os
import requests
import json 

# API Tokens 
nasa_lance_token = 'C751EA24-F34E-11E9-9D0F-ABF3207B60E0'
open_weather_token = ''


# Functions 

def get_lon():
    pass

def get_lat():
    pass

def get_firms():
    lance_firms_url = 'https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS'
    lance_firms_wget = f'wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 "{lance_firms_url}" --header "Authorization: Bearer {nasa_lance_token}" -P ../../'
    return os.system(lance_firms_wget)

def get_weather(lon, lat):
    open_weather_url = f'api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon} '
    response = requests.get(open_weather_url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
    
    
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