import utils.dt_routing as dt_rt
import utils.utils as utils
import json
import pandas as pd
from shapely.geometry import Point, LineString, Polygon

def getItinDuration(itin):
    return itin['duration']

def get_best_itins(origin, dest_coords, bikeSpeed, routes):
    datetime = utils.get_next_weekday_datetime(8, 45)
    itins = dt_rt.get_route_itineraries(origin, dest_coords, bikeSpeed, 6000, 4, datetime)
    itins = dt_rt.parse_itin_geom(itins)
    sorted_itins = sorted(itins, key=getItinDuration)
    # print(sorted_itins)
    return sorted_itins

def asMinutes(seconds):
    return int(round(seconds/60))

def get_bike_df(row, population, itin, tt_norm):
    hsy_idx = row['INDEX']
    bike = itin['legs'][0]
    tt = asMinutes(itin['duration'])
    tt_diff = asMinutes(tt_norm - itin['duration'])
    b_distance = int(round(bike['distance']))
    b_duration = asMinutes(bike['duration'])
    arrow = LineString([bike['first_point'], bike['last_point']])
    saved_min = asMinutes(population * (tt_norm - itin['duration']))

    all_br_data = pd.DataFrame(data={'hsy_idx': [hsy_idx], 'pop': [population], 'tt': [tt], 'tt_diff': [tt_diff], 'saved_min': [saved_min], 'b_distance': [b_distance], 'b_duration': [b_duration], 'first_point': [bike['first_point']], 'last_point': [bike['last_point']], 'last_p_str': [str(bike['last_point'])], 'arrow': [arrow], 'bike_geom': [bike['line_geom']] })
    return all_br_data

def get_bike_ride_effect(row, dest_coords):
    population = row['ASUKKAITA']
    geom = row['geometry']
    fromLatLon = {'lat': geom.y, 'lon': geom.x }

    walkSpeed = '1.33'
    datetime = utils.get_next_weekday_datetime(8, 45)
    tt_norm = dt_rt.get_mean_travel_time(fromLatLon, dest_coords, walkSpeed, 6000, 3, False, datetime)

    br_itins = get_best_itins(fromLatLon, dest_coords, '4.33', 4)
    itin1 = br_itins[0]
    itin2 = br_itins[1]
    b1 = itin1['legs'][0]
    b2 = itin2['legs'][0]
    
    if (str(b1['last_point']) != str(b2['last_point'])):
        population = int(round(population/2))
        br_df1 = get_bike_df(row, population, itin1, tt_norm)
        br_df2 = get_bike_df(row, population, itin2, tt_norm)
        return pd.concat([br_df1, br_df2])
    else:
        return get_bike_df(row, population, itin1, tt_norm)
