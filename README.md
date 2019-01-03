# Final Assignment
Read the final assignment instructions from the [https://autogis.github.io](https://automating-gis-processes.github.io/2018/lessons/FA/final-assignment.html).

You should upload all your code(s) / notebook(s) into this repository and write a **good documentation** how everything works.

# Multi-Stop Route Optimizer Tool
## Introduction 
The multi-stop route optimizer is a command line interface/tool that will solve shortest route between multiple stops. Shortest route is calculated based on travel times extracted from [Helsinki Region Travel Time Matrix 2018](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2018/). 

## Features
First, the program geocodes user defined locations using [Digitransit Geocoding API](https://digitransit.fi/en/developers/apis/2-geocoding-api/). Geocoded locations are saved as a shapefile and can be imported to the program on a later run instead of geocoding new locations. After user has accepted the geocoding results, the program proceeds to find all possible combinations (permutations) of stops. Subsequently, total travel times of all stop-combinations are extracted and combined from travel time matrix. Optionally, user can define fixed origin and destination stops. Finally, best routes are selected and printed based on shortest total travel time.

[See an use case example from here.](example_route_1.md)

## Installation
Set up the python environment with the following commands:
```
$ conda create -n geoenv -c conda-forge python=3.6.5 jupyterlab geopandas geoplot osmnx pysal contextily
$ pip install pycrs
$ pip install requests
$ conda activate geoenv
```
Add [travel time matrix](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2018/)
 to the path `/data/HelsinkiTravelTimeMatrix2018`

## Running the program
```
$ conda activate geoenv
$ cd final-assignment-hellej
$ python route_planner_app.py 
```
