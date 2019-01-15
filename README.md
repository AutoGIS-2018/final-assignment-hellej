Read the final assignment instructions from the [https://autogis.github.io](https://automating-gis-processes.github.io/2018/lessons/FA/final-assignment.html).

## Table of Contents
<!--ts-->
* [Multi-Stop Route Optimizer Tool](#multi-stop-route-optimizer-tool)
  * [Introduction](#introduction)
  * [Usage](#usage)
  * [Installation](#installation)
  * [Starting the program](#starting-the-program)
  * [Components](#components)
* [Analysis for bike & ride potential using Digitransit Routing API](#analysis-for-bike--ride-potential-using-Digitransit-Routing-API)
  * [Background](#background)
  * [Data & Methods](#data--methods)
  * [Results & interpretation of the map visualization](#results--interpretation-of-the-map-visualization)
  * [Discussion - how to further develop the analysis?](#discussion---how-to-further-develop-the-analysis)
  * [Map of bike & ride potential in Koskela](#map-of-bike--ride-potential-in-koskela)
* [License](LICENSE)
  <!--te-->

# Multi-Stop Route Optimizer Tool
## Introduction
This final assignment aims to solve a very practical problem that almost everyone is likely to face at some point of their lives. For example, a group of friends is willing to visit each other's homes during one evening (but are uncertain about the optimal sequence) or perhaps you just want to know the fastest route to sequentially visit home, a grocery store, a post office and a library... 

This program can be used to solve multi-stop route optimization problem by minimizing total travel time of itineraries. The implementation is a command line interface/tool that will read all necessary user inputs (such as addresses of the stops) from keyboard. Travel times are extracted either from [Helsinki Region Travel Time Matrix 2018](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2018/) or [Digitransit Routing API](https://digitransit.fi/en/developers/apis/1-routing-api/). 

## Usage
First, the program geocodes user defined locations by using [Digitransit Geocoding API](https://digitransit.fi/en/developers/apis/2-geocoding-api/). Geocoded locations are saved as a shapefile and can be imported to the program on a later run (instead of geocoding new locations). After user has accepted the geocoding results, the program proceeds to find all possible combinations (permutations) of stops. Subsequently, total travel times of all stop-combinations are extracted and combined from either the [travel time matrix](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2018/) or [Digitransit Routing API](https://digitransit.fi/en/developers/apis/1-routing-api/). Optionally, user can define fixed origin and/or destination. Finally, best routes are selected and printed. 

[See some example runs from here.](demo/route-optim-outputs.md)

## Installation
Set up the python environment with the following commands:
```
$ conda create -n geoenv -c conda-forge python=3.6.5 jupyterlab geopandas geoplot pysal
$ pip install pycrs
$ pip install requests
$ pip install polyline
```
Add the [travel time matrix](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2018/)
 to the path `/data/HelsinkiTravelTimeMatrix2018`

## Starting the program
```
$ git clone git@github.com:AutoGIS-2018/final-assignment-hellej.git
$ conda activate geoenv
$ cd final-assignment-hellej
$ python route_planner_app.py
```

## Components
``` 
  ├── data
  │   ├── HelsinkiTravelTimeMatrix2018/ */ *.txt     
  │   └── MetropAccessGrid/ *.shp
  ├── demo 
  │   ├── * .py                     # Jupyter notebook like scripts to run with VSCode
  │   ├── bike_ride_potential.py    # Example analysis for bike & ride potential in Koskela
  │   ├── dt_geocode.py             # Geocode address using utils.dt_geocode.py
  │   ├── dt_routing.py             # Get route using utils.dt_routing.py
  │   ├── optimize_route.py         # Optimize multi-stop route
  │   └── route-optim-outputs.md    # Example outputs of route_planner_app.py
  ├── input
  │   └── *.shp                     # Optional locations to use in multi-stop route optimization
  ├── utils                         # Utils-module
  │   ├── bike_ride_potential.py    # Utils for querying and processing bike & ride routes
  │   ├── dt_geocode.py             # Utilization of Digitransit Geocoding API
  │   ├── dt_routing.py             # Utilization of Digitransit Routing API
  │   ├── routes_tt.py              # Forming and comparing multi-stop route options
  │   ├── times.py                  # Creating and handling datetime objects
  │   ├── travel_times.py           # Collecting travel times from travel time matrixes or Digitransit API
  │   └── user_inputs.py            # Asking and validating keyboard inputs
  │── demo_geocoding.ipynb
  │── demo_route_optim.ipynb
  │── demo_routing.ipynb
  └── route_planner_app.py          # Main application, run this in terminal
```

# Analysis for bike & ride potential using Digitransit Routing API
Also, a smaller (stand-alone) side project was composed as a proof of concept of spatial analysis for bike & ride potential using Digitransit Routing API. Koskela was selected as the study area for developing and testing the analysis. Being less connected to fast PT routes than the surrounding neighborhoods (e.g. Kumpula & Käpylä), considerable bike & ride potential was anticipated for the area. The analysis aims to identify most potential bike & ride hubs and quantify population of their catchment areas.

## Background
The analysis is based on the following assumptions:
* Significant proportion of potential bike & ride hubs get considered if routing is done towards Helsinki Central Station
* Cycling can be modelled as fast walking (in routing)
* Average cycling speed is 16.6 km/h
* It takes additional 30 s to both get the bike and lock it at the destination
* It takes additional 2 min to walk from the bicycle stand to the station/stop

## Data & Methods
The [analysis](demo/bike_ride_potential.py) utilizes [these functions](utils/bike_ride_potential.py) and proceeds roughly with the following logic:
1) Polygon centers are extracted from HSY's 250m population grid
2) Center points that fall inside the area of interest (Koskela polygon) are selected for analysis
3) Routing is executed from each point to Helsinki Central Station
4) In the routing, walking speed is set as cycling speed
5) From the returned four itineraries, two fastest are selected for further processing
6) The first legs of the itineraries are taken as cycling
7) If the first legs of the two routes are to different stations, both of them are analyzed
8) Cumulative reached population and average time saved are aggregated for each bike & ride hub
9) Results are visualized as a map

## Results & interpretation of the [map visualization](#map-of-bike--ride-potential-in-koskela)
The results of the analysis include several travel time and population metrics and are saved as [multiple shapefiles](demo/output) with varying geometries (hub/origin/route). Short descriptions of the result files and their attributes are in the file [br_files_fields.md](demo/output/br_files_fields.md).

* Straight lines between origins and bike & ride hubs represent cycling legs that reduce total travel time by at least 9 minutes
* Two most prominent bike & ride hubs for the AOI can be identified: Käpylä & Oulunkylä train stations
* Labels above the origins show saved minutes (from choosing bike & ride itinerary)
* If origin is connected to two hubs, saved time (min) is only shown for the faster itinerary
* Choosing bike & ride itinerary (instead of normal walk & ride itinerary) has the potential to reduce travel times from 8 to 15 minutes (to city center)
* Greatest benefits from bike & ride itineraries are located near the center of the AOI where proximity to trunk routes of PT is the furthest

## Discussion - how to further develop the analysis?
* Multiple targets should be used in the analysis (i.e. not just Helsinki Central Station)
* Better considerations of parameters of the analysis are required (cycling speed, locking time, transfer costs etc.)
* More advanced routing for cycling should be used (Digitransit API provides some options)
* Also frequency of departures from different stations should be considered in assessing their feasibility as bike & ride hubs
* Analysis for the whole municipality?

## Map of bike & ride potential in Koskela
![bike_ride_potential_koskela](demo/output/koskela_br.png)

## License
[MIT](LICENSE)
