# Wildfire Watch (Lambda Labs 17)
You can find the project at [WildfireWatchApp.com](https://www.wildfirewatchapp.com/).

## Contributors
### (Left to Right)
 
| **Chance Dare:** [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/ChanceDurr) [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/chancedare) | **Eric Wuerfel:** [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/eWuerfel66) [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/eric-wuerfel/) |                                  **Ned Horsey:** [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Rice-from-data) [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/edmond-horsey) | **Liv Johnson:** [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/livjab) [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/liv-johnson-015523144/) | **Oscar Calzada:** [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/ocalzada) [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://linkedin.com/in/oscar-calzada-b34b8b53)|          
**Vishnu Yarmaneni:** [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/vishnuyar) [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://linkedin.com/in/vishnuvyarmaneni)

|                      [<img src="https://avatars2.githubusercontent.com/u/46852089?s=400&v=4" width = "200" />](https://github.com/ChanceDurr)                       |                      [<img src="https://avatars0.githubusercontent.com/u/37782589?s=400&v=4" width = "200" />](https://github.com/ewuerfel66)                       |                      [<img src="https://avatars1.githubusercontent.com/u/44828872?s=460&v=4" width = "200" />](https://github.com/Rice-from-data)                       |                      [<img src="https://avatars2.githubusercontent.com/u/23245487?s=460&v=4" width = "200" />](https://github.com/livjab)                       |
[<img src="https://avatars1.githubusercontent.com/u/53792042?s=460&v=4" width = "200" />](https://github.com/ocalzada)                       |[<img src="https://avatars3.githubusercontent.com/u/3436873?s=460&v=4" width = "200" />](https://github.com/vishnuyar)                       |

![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Project Overview

[Trello Board](https://trello.com/b/OVbzoexc/labs17-forest-fire-watch)

[Product Canvas](https://www.notion.so/dd55f670427b40f7bc0503e36ad58ea9?v=d4cc255c2ad341a1b2ccd03f0d8d86f9)

### Problem

 - It's hard to be aware of wildfires in your area because the data compiled for government use is confusing.
 - Local alerts for wildfires can fail in emergencies.
 - If you aren't generally aware of wildfire risk, you won't be ready in a disaster situation.
 
### Objectives
 
 - Provide an easy way to be aware of wildfires in your area.

### Tech Stack

SQL, Psycopg2, Python, Pandas, Flask, Feedparser

### Data

#### MODIS Data
-   Brightness - Brightness temperature 21 (Kelvin) 
-   Scan - Along Scan pixel size 
-   Track - Along Scan pixel size
-   Acq_Date - Acquisition Date 
-   Acq_Time  - Acquisition Time 
-   Satellite - A = Aqua and T = Terra
-   Confidence - Confidence (0-100%) 
-   Bright_T31 - Brightness temperature 31 (Kelvin) 
-   FRP - Fire Radiative Power (MW - megawatts) 
-   DayNight  - Day or Night 
-   Clusters - Binary Y/N if pixel is part of a clutser

#### Weather Data
-   Temperature - (Fahrenheit)
-   Wind Speed - (MPH)
-   Wind Direction - (Degrees, Due North)

### Data Sources

-   [Inciweb RSS Feed](https://inciweb.nwcg.gov/feeds/rss/incidents/)
-   [MODIS Data](https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv)
-   [Weather API](http://api.openweathermap.org/data/2.5/weather?)
-   [Air Quality API](https://openaq.org/#/?_k=ww3pis)
-   [API World's Air Pollution: Real-time Air Quality Index](https://waqi.info/)

#### Data Sources not Used
-   [US Wildfires](https://www.kaggle.com/rtatman/188-million-us-wildfires)
-   [NASA Satellite FIRMS Data](https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt)
-   [MCD14DL](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/c6-mcd14dl#ed-firms-attributes)
-   [Federal Fire Occurrence Website](https://wildfire.cr.usgs.gov/firehistory)
-   [NOAA GLOBAL HISTORICAL CLIMATOLOGY NETWORK](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-monthly-version-4)

### How to access our Current Fires API
- Our Current Fires API is deployed at: https://wildfirewatch.herokuapp.com/

#### /fpfiretype
- Methods: ["GET"]
- Returns: `[{'name': "Fire Name", 'type': "Wildfire", 'location': [lat, lon]}, ...]`

#### /check_rss_fires
- Methods: ["POST"]
- Request JSON Format:
```
{
	"position": [lat, lon],
	"radius": int
}
```
- Returns: 
```
{
	'nearby_fires': [{'name': "Fire Name", 'location': [lat, lon]}, ...],
	'other_fires': [{'name': "Fire Name", 'location': [lat, lon]}, ...]
}
```
#### /get_aqi_data
- Methods: ["GET"]
- Request JSON Format:
```
{
	"lat": latitude value,
	"lng": longitude value
}
```
- Returns: 
```
{  "aqi": value, co": {"v": value}, "no2": {"v": value}, "o3": {"v": value}, "p": {"v": value }, "pm10": {"v": value  }, 
  	   "pm25": {"v": value}, "so2": {"v": value}, "t": {"v": value}, "w": {"v": value}
}

```

#### /get_aqi_stations
- Methods: ["GET"]
- Request JSON Format:
```
{
	"lat": latitude value,
	"lng": longitude value.
	"distance": distance value
}
```
- Returns: 
```
{
  "data": [ { "aqi": "-", "lat": value, "lon": value, 
      "station": {"name": value, "time": value  }, 
      "uid": value
    }], 
  "status": "ok"
}

```

### How to connect to our Training Database
- Our database is hosted on ElephantSQL.
- Our training DB has all the features listed in the **Data** section above, and is labeled `1` for `fire`, `0` for `no fire`.

Here are the public credentials:
```
# Credentials
dbname = 'iagqhysc'
user = 'iagqhysc'
password = '*****'
host = 'salt.db.elephantsql.com'
```
Please contact the creators for the password.

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./CODE_OF_CONDUCT.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Documentation

See [Backend Documentation](https://github.com/Lambda-School-Labs/forest-fire-watch-be) for details on the backend of our project.

See [Front End Documentation](https://github.com/Lambda-School-Labs/forest-fire-watch-fe) for details on the front end of our project.
