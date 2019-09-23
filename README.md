# FireFlight
You can find the project at [FireFlightApp.com](https://www.fireflightapp.com/).

## Contributors

|                                       [Ned Horsey](https://github.com/Rice-from-data)                                        |                                       [Liv Johnson](https://github.com/livjab)                                        |                                       [](https://github.com/)                                        |
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="https://avatars1.githubusercontent.com/u/44828872?s=460&v=4" width = "200" />](https://github.com/Rice-from-data)                       |                      [<img src="https://avatars2.githubusercontent.com/u/23245487?s=460&v=4" width = "200" />](https://github.com/livjab)                       |                                             |                                             |                                             |
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Rice-from-data)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/livjab)             |                         |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/edmond-horsey) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/liv-johnson-015523144/) |  |


![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Netlify Status](https://api.netlify.com/api/v1/badges/b5c4db1c-b10d-42c3-b157-3746edd9e81d/deploy-status)](https://fireflight.netlify.com/)

## Project Overview

[Trello Board](https://trello.com/b/LHd7GbuL/labs15-forest-fire)

[Product Canvas](https://www.notion.so/dd55f670427b40f7bc0503e36ad58ea9?v=d4cc255c2ad341a1b2ccd03f0d8d86f9)

### Problem
 - It's hard to be aware of wildfires in your area because all data is compiled for government use.
 - Local alerts for wildfires can fail in emergencies.
 - If you aren't generally aware of wildfire risk, you won't be ready in a disaster situation.
 
### Objectives
 
 - Provide an easy way to be aware of wildfires in your area.
 
[Deployed Front End](https://fireflight.netlify.com/)

### Tech Stack

SQL, Python, Pandas, Scikit-learn, XGB, HDBSCAN, Flask

### Classification Model

A model has been created using historic NASA satellite data, matched by date and location to known wildfires within the US. We are using this labled data in conjunction with NASA's current active fire data to correctly classify wildfires from live satellite image data. 

### 2️⃣ Explanatory Variables

-   Brightness - Brightness temperature 21 (Kelvin) 
-   Scan - Along Scan pixel size 
-   Track - Along Scan pixel size
-   Acq_Date - Acquisition Date 
-   Acq_Time  - Acquisition Time 
-   Satellite -  	A = Aqua and T = Terra
-   Confidence - Confidence (0-100%) 
-   Bright_T31 - Brightness temperature 31 (Kelvin) 
-   FRP - Fire Radiative Power (MW - megawatts) 
-   DayNight  - Day or Night 
-   Clusters - Binary Y/N if pixel is part of a clutser


### Data Sources


-   [US Wildfires](https://www.kaggle.com/rtatman/188-million-us-wildfires)
-   [NASA Satellite FIRMS Data](https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt)
-   [MCD14DL](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/c6-mcd14dl#ed-firms-attributes)
-   [Federal Fire Occurrence Website](https://wildfire.cr.usgs.gov/firehistory)
-   [NOAA GLOBAL HISTORICAL CLIMATOLOGY NETWORK](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-monthly-version-4)

### Python Notebooks

🚫  Add to or delete python notebook links as needed for your project

[Python Notebook 1](🚫add link to python notebook here)

[Python Notebook 2](🚫add link to python notebook here)

[Python Notebook 3](🚫add link to python notebook here)

### 3️⃣ How to connect to the web API

🚫 List directions on how to connect to the API here

### 3️⃣ How to connect to the data API

🚫 List directions on how to connect to the API here

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md.md). Please follow it in all your interactions with the project.

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

See [Backend Documentation](https://github.com/labs15-forest-fire/backend) for details on the backend of our project.

See [Front End Documentation](https://github.com/labs15-forest-fire/frontend) for details on the front end of our project.
