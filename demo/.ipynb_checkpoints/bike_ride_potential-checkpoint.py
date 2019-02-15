
# Proof of concept:
# Analysis for bike & ride potential in Koskela, northern Helsinki

#%%
import pandas as pd
import geopandas as gpd
import utils.bike_ride_potential as br_utils
from fiona.crs import from_epsg
import sys

#%%
# read population data
pop_poly = gpd.read_file('data/hsy_vaesto_2017/Vaestoruudukko_2017.shp')
koskela_poly = gpd.read_file('data/koskela/koskela.shp')
dest_coords = { 'lat': 60.170435, 'lon': 24.940673 } # Helsinki railvay station

#%%
# extract center points of population grid
pop_point = pop_poly.copy()
pop_point['geometry'] = [geom.centroid for geom in pop_point['geometry']]
pop_point = pop_point.to_crs(from_epsg(4326))

#%%
# select only points inside AOI (Koskela-polygon)
point_mask = pop_point.intersects(koskela_poly.loc[0, 'geometry'])
pop_koskela = pop_point.loc[point_mask].reset_index(drop=True)

#%% 
# set time penalties for unlocking, locking and walking to the station
unlock_lock_t = 60
walk_station_t = 120

#%%
# get and collect all bike & ride routes & travel times 
br_dfs = []
row_count = len(pop_koskela.index)
print('Get bike & ride itineraries: ')
for index, row in pop_koskela.iterrows():
    sys.stdout.write(str(index+1)+'/'+str(row_count)+' ')
    sys.stdout.flush()
    br_dfs.append(br_utils.get_bike_ride_feature(row, dest_coords, unlock_lock_t, walk_station_t))
br_df = pd.concat(br_dfs)

#%%
# attributes of bike & ride features
cols = ['hsy_idx', 'pop', 'tt_norm', 'tt_br', 'tt_diff', 'tt_ratio', 'saved_min', 'tt_b', 'dist_b', 'last_p_str']
print(br_df[cols].head())

#%%
# save bike & ride features as shapefiles with different geometries:

# cycling routes as simple origin-destination lines
br_lines_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['arrow'], crs= from_epsg(4326))
br_lines_gdf.to_file('demo/output/br_lines.shp')

# all cycling routes as lines
br_routes_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['bike_geom'], crs= from_epsg(4326))
br_routes_gdf.to_file('demo/output/br_routes.shp')

#%%
# origins of cycling routes = center points of HSY population grid
br_origins_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['first_point'], crs= from_epsg(4326))
# group and summarize br travel times from origins based on HSY idx
grouped = br_origins_gdf.groupby('hsy_idx')
orig_gdfs = []
rownum = 0
for key, values in grouped:
    pop = list(values['pop'])[0]
    tt_norm = list(values['tt_norm'])[0]
    tt_br = values['tt_br'].min()
    tt_diff = values['tt_diff'].max()
    tt_ratio = values['tt_ratio'].max()
    geom = list(values['geometry'])[0]
    orig_gdf = gpd.GeoDataFrame(data={'rownum': rownum, 'pop': [pop], 'tt_norm': [tt_norm], 'tt_br': [tt_br], 'tt_diff': [tt_diff], 'tt_ratio': [tt_ratio]}, geometry=[geom], crs=from_epsg(4326))
    orig_gdfs.append(orig_gdf)
    rownum += 1
br_origins_gdf = pd.concat(orig_gdfs).reset_index(drop=True)
br_origins_gdf.to_file('demo/output/br_origins.shp')

#%%
# all cycling destinatinos (PT hubs: stations/stops)
br_hubs_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['last_point'], crs= from_epsg(4326))
br_hubs_gdf.to_file('demo/output/br_hubs.shp')
# group and summarize hubs based on last point of the first transit leg (cycling)
grouped = br_hubs_gdf.groupby('last_p_str')
hub_dfs = []
rownum = 0
for key, values in grouped:
    sum_pop = values['pop'].sum()
    sum_saved_tt = values['saved_min'].sum()
    avg_saving = sum_saved_tt / sum_pop
    geom = list(values['geometry'])[0]
    hub_gdf = gpd.GeoDataFrame(data={'rownum': rownum, 'sum_pop': [sum_pop], 'sum_saved_tt': sum_saved_tt, 'avg_saving': [avg_saving]}, geometry=[geom], crs=from_epsg(4326))
    hub_dfs.append(hub_gdf)
    rownum += 1
hub_sum_gdf = pd.concat(hub_dfs).reset_index(drop=True)
print(hub_sum_gdf)

#%%
# group and summarize adjacent hubs
br_sum_hubs_gdf = br_utils.group_summarize_adjacent_hubs(hub_sum_gdf, 250)
br_sum_hubs_gdf.to_file('demo/output/br_sum_hubs.shp')
