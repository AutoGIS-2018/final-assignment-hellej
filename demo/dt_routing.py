# Digitransit Routing API DEMO

#%%
import geopandas as gpd
import utils.dt_routing as routing
from shapely.geometry import Point, LineString
from datetime import datetime

# route params for testing
coords_from = {'lat': 60.168992, 'lon': 24.932366 }
coords_to = {'lat': 60.175294, 'lon': 24.684855 }
walkSpeed = '1.33'
maxWalkDistance = 6000

#%%
# build and run routing query
itins = routing.get_route_itineraries(coords_from, coords_to, walkSpeed, maxWalkDistance, 3, datetime.now())
# parse geometry from Google Encoded Polyline Algorithm Format
itins_geom = routing.parse_itin_geom(itins)

#%%
# print route geometry (line) of the first itinerary
itin = itins_geom[0]
itin['line_geom']

#%%
# get only travel time
tt = routing.get_mean_travel_time(coords_from, coords_to, walkSpeed, maxWalkDistance, 3, True, datetime.now())
print(tt)

#%%
