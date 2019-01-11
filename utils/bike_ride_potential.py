import utils.dt_routing as dt_rt
import utils.utils as utils
import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
from fiona.crs import from_epsg

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
    tt_br = asMinutes(itin['duration'])
    tt_b = asMinutes(bike['duration'])
    tt_diff = asMinutes(tt_norm - itin['duration'])
    dist_b = int(round(bike['distance']))
    arrow = LineString([bike['first_point'], bike['last_point']])
    saved_min = asMinutes(population * (tt_norm - itin['duration']))

    br_df = pd.DataFrame(data={'hsy_idx': [hsy_idx], 'pop': [population], 'tt_norm': [tt_norm], 'tt_br': [tt_br], 'tt_diff': [tt_diff], 'saved_min': [saved_min], 'tt_b': [tt_b], 'dist_b': [dist_b], 'first_point': [bike['first_point']], 'last_point': [bike['last_point']], 'last_p_str': [str(bike['last_point'])], 'arrow': [arrow], 'bike_geom': [bike['line_geom']] })
    return br_df

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

def group_summarize_adjacent_hubs(hub_sum_gdf, distance):
    # set radius of the buffer
    radius = distance/2
    # reproject
    hub_sum_gdf = hub_sum_gdf.to_crs(epsg=3879)
    # reset index
    hub_sum_gdf= hub_sum_gdf.reset_index(drop=True)
    # add buffers
    hub_sum_gdf['buffer'] = [geom.buffer(radius) for geom in hub_sum_gdf['geometry']]
    
    # function for determining if hub is already allocated to group or not
    def not_in_any_hub_group(groups, index):
        for group in groups:
            if index in group:
                return False
        return True

    # collect groups of adjacent hubs
    groups = []
    for idx, row in hub_sum_gdf.iterrows():
        group = []
        if (not_in_any_hub_group(groups, idx)):
            group.append(idx)
        buffer = row['buffer']
        for compare_idx, compare_row in hub_sum_gdf.iterrows():
            if (idx == compare_idx):
                print('skipping same point')
                continue
            if (buffer.intersects(compare_row['buffer'])):
                print('found intersecting buffers')
                if (not_in_any_hub_group(groups, compare_idx)):
                    print('add intersecting hub to same group')
                    group.append(compare_idx)
                else:
                    print('intersecting hub already in a group')
        groups.append(group)

    groups = [group for group in groups if len(group)>0]
    print(groups)

    # add group id to a column
    def get_hub_group(row, groups):
        for idx, group in enumerate(groups):
            if (row['rownum'] in group):
                return idx
        return '9999'
    hub_sum_gdf['h_group'] = hub_sum_gdf.apply(lambda row: get_hub_group(row, groups), axis=1)

    # re-summarize hubs based on groups of adjacent hubs
    grouped = hub_sum_gdf.groupby('h_group')
    hub_dfs = []
    rownum = 0
    for key, values in grouped:
        sum_pop = values['sum_pop'].sum()
        sum_saved_tt = values['sum_saved_tt'].sum()
        avg_saving = sum_saved_tt / sum_pop
        geom = list(values['geometry'])[0]
        hub_gdf = gpd.GeoDataFrame(data={'rownum': rownum, 'sum_pop': [sum_pop], 'sum_saved_tt': sum_saved_tt, 'avg_saving': [avg_saving]}, geometry=[geom], crs=from_epsg(3879))
        hub_dfs.append(hub_gdf)
        rownum += 1
    hub_sum_gdf = pd.concat(hub_dfs).reset_index(drop=True)
    print(hub_sum_gdf)

    return hub_sum_gdf
