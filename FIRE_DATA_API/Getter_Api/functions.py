
# System Imports
import os
import requests
import json 

# URLs 
lance_firms_wget = 'wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 "https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS" --header "Authorization: Bearer C751EA24-F34E-11E9-9D0F-ABF3207B60E0" -P ../../'

# Functions 
def get_firms():
    os.system(lance_firms_wget)
    pass

def get_weather():
    pass
