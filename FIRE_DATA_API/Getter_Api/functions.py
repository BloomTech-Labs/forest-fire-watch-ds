
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


## Notes 

# prob need a function to check if  user input is within an already checked radius
# so as not to exceed request limit of Open weather data. 

# open weather has a retangular box api call that may solve this problem 