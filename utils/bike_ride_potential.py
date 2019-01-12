import utils.dt_routing as dt_rt
import utils.times as t_utils
import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
from fiona.crs import from_epsg

def getItinDuration(itin):
    return itin['duration']

def as_min(seconds):
    return int(round(seconds/60))

def get_cycling_leg_df(row, population, itin, tt_norm, add_t):
    # collect itinerary information (population, travel times and potential travel time savings with bike & ride)
    # also add several geometry columns to the returned DF
    hsy_idx = row['INDEX']
    bike = itin['legs'][0]
    tt_b = bike['duration'] + add_t
    tt_br = itin['duration'] + add_t
    tt_diff = tt_norm - tt_br
    tt_ratio = int(round((tt_diff/tt_norm)*100))
    tt_total_saved = population * tt_diff
    dist_b = int(round(bike['distance']))
    arrow = LineString([bike['first_point'], bike['last_point']])

    br_df = pd.DataFrame(data={'hsy_idx': [hsy_idx], 'pop': [population], 'tt_norm': [as_min(tt_norm)], 'tt_br': [as_min(tt_br)], 'tt_diff': [as_min(tt_diff)], 'tt_ratio': [tt_ratio], 'saved_min': [as_min(tt_total_saved)], 'tt_b': [as_min(tt_b)], 'dist_b': [dist_b], 'first_point': [bike['first_point']], 'last_point': [bike['last_point']], 'last_p_str': [str(bike['last_point'])], 'arrow': [arrow], 'bike_geom': [bike['line_geom']] })
    return br_df

def get_bike_ride_feature(row, dest_coords, unlock_lock_t, walk_station_t):
    add_t = unlock_lock_t + walk_station_t
    population = row['ASUKKAITA']
    fromLatLon = {'lat': row['geometry'].y, 'lon': row['geometry'].x }

    # get reference travel time with default routing parameters
    walkSpeed = '1.33'
    datetime = t_utils.get_next_weekday_datetime(8, 45)
    tt_norm = dt_rt.get_mean_travel_time(fromLatLon, dest_coords, walkSpeed, 6000, 3, False, datetime)

    # Request and process bike & ride itineraries
    cycl_speed = '4.33'
    datetime = t_utils.get_next_weekday_datetime(8, 45)
    itins = dt_rt.get_route_itineraries(fromLatLon, dest_coords, cycl_speed, 6000, 4, datetime)
    itins = dt_rt.parse_itin_geom(itins)
    br_itins = sorted(itins, key=getItinDuration)

    # extract cycling legs from the itineraries
    itin1 = br_itins[0]
    itin2 = br_itins[1]
    b1 = itin1['legs'][0]
    b2 = itin2['legs'][0]

    # check if cycling legs of the two best itineraries are the same
    if (str(b1['last_point']) != str(b2['last_point'])):
        # return both cycling legs, half of the population allocated to each of them 
        population = int(round(population/2))
        br_df1 = get_cycling_leg_df(row, population, itin1, tt_norm, add_t)
        br_df2 = get_cycling_leg_df(row, population, itin2, tt_norm, add_t)
        return pd.concat([br_df1, br_df2])
    else:
        # return only one cycling leg
        return get_cycling_leg_df(row, population, itin1, tt_norm, add_t)

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

    # collect groups of adjacent hubs based on possibly intersecting buffers
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
