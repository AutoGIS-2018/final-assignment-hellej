
# Proof of concept:
# Analysis for bike & ride potential in Koskela, northern Helsinki

#%%
import pandas as pd
import geopandas as gpd
import utils.bike_ride_potential as br_utils
from fiona.crs import from_epsg
# from shapely.geometry import Point, MultiPoint

#%%
# read population data
pop_poly = gpd.read_file('data/hsy_vaesto_2017/Vaestoruudukko_2017.shp')
koskela_poly = gpd.read_file('data/koskela/koskela.shp')
dest_coords = { 'lat': 60.170435, 'lon': 24.940673 } # Helsinki railvay station

#%%
pop_point = pop_poly.copy()
pop_point['geometry'] = [geom.centroid for geom in pop_point['geometry']]
pop_point = pop_point.to_crs(from_epsg(4326))

#%%
# select only points inside AOI (Koskela-polygon)
point_mask = pop_point.intersects(koskela_poly.loc[0, 'geometry'])
pop_koskela = pop_point.loc[point_mask]

#%%
# select one point for testing
test_point = pop_koskela[pop_koskela['INDEX'] == 17420].reset_index()

#%% 
# get and collect all bike & ride (br) routes
br_dfs = [br_utils.get_bike_ride_effect(row, dest_coords) for index, row in pop_koskela.iterrows()]
br_df = pd.concat(br_dfs)

#%%
cols = ['hsy_idx', 'pop', 'tt_norm', 'tt_br', 'tt_diff', 'saved_min', 'tt_b', 'dist_b', 'last_p_str']
br_lines_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['arrow'], crs= from_epsg(4326))
br_lines_gdf.to_file('demo/output/br_lines.shp')

br_routes_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['bike_geom'], crs= from_epsg(4326))
br_routes_gdf.to_file('demo/output/br_routes.shp')

br_origins_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['first_point'], crs= from_epsg(4326))
br_origins_gdf.to_file('demo/output/br_origins.shp')

br_hubs_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['last_point'], crs= from_epsg(4326))
br_hubs_gdf.to_file('demo/output/br_hubs.shp')

#%%
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
br_sum_hubs_gdf = br_utils.group_summarize_adjacent_hubs(hub_sum_gdf, 250)
br_sum_hubs_gdf.to_file('demo/output/br_sum_hubs.shp')







# #%%
# # project and collect destinations as list
# hub_sum_gdf['buffer'] = [geom.buffer(150.0) for geom in hub_sum_gdf['geometry']]

# #%%
# def not_in_any_hub_group(groups, index):
#     for group in groups:
#         if index in group:
#             return False
#     return True

# # collect aggregated groups of hubs grom adjacent hubs
# groups = []
# for idx, row in hub_sum_gdf.iterrows():
#     group = []
#     if (not_in_any_hub_group(groups, idx)):
#         group.append(idx)
#     buffer = row['buffer']
#     for compare_idx, compare_row in hub_sum_gdf.iterrows():
#         if (idx == compare_idx):
#             print('skipping same point')
#             continue
#         if (buffer.intersects(compare_row['buffer'])):
#             print('found intersecting buffers')
#             if (not_in_any_hub_group(groups, compare_idx)):
#                 print('add intersecting hub to same group')
#                 group.append(compare_idx)
#             else:
#                 print('intersecting hub already in a group')
#     groups.append(group)

# groups = [group for group in groups if len(group)>0]
# print(groups)

# #%%
# # add hub new group ids to summarized hubs
# def get_hub_group(row, groups):
#     for idx, group in enumerate(groups):
#         if (row['rownum'] in group):
#             return idx
#     return '9999'

# hub_sum_gdf['h_group'] = hub_sum_gdf.apply(lambda row: get_hub_group(row, groups), axis=1)
# print(hub_sum_gdf)

# # re-summarize hubs based on groups of adjacent hubs
# #%%
# grouped = hub_sum_gdf.groupby('h_group')
# hub_dfs = []
# rownum = 0
# for key, values in grouped:
#     sum_pop = values['sum_pop'].sum()
#     sum_saved_tt = values['sum_saved_tt'].sum()
#     avg_saving = sum_saved_tt / sum_pop
#     geom = list(values['geometry'])[0]
#     hub_gdf = gpd.GeoDataFrame(data={'rownum': rownum, 'sum_pop': [sum_pop], 'sum_saved_tt': sum_saved_tt, 'avg_saving': [avg_saving]}, geometry=[geom], crs=from_epsg(3879))
#     hub_dfs.append(hub_gdf)
#     rownum += 1
# hub_sum_gdf = pd.concat(hub_dfs).reset_index(drop=True)
# print(hub_sum_gdf)










#%%
#%%
# hub_sum_gdf = br_hubs_gdf.to_crs(epsg=3879) 
# dests = list(hub_sum_gdf['geometry'])
# destPoints = MultiPoint(dests)
# print(destPoints)
#%

# dests = []
# hubs = {}
# for key, values in grouped:
#     projected = values.to_crs(epsg=3857)
#     point = list(projected['geometry'])[0]
#     dests.append(point)

# #%%
# for key, values in grouped:
#     projected = values.to_crs(epsg=3857)
#     point = list(projected['geometry'])[0]
#     print('point:', point)
#     f_dests = [dest for dest in dests if str(dest) != str(point)]
#     destPoints = MultiPoint(f_dests)
#     # print('destPoints:', destPoints)
#     nearest = nearest_points(point, destPoints)[1]
#     print('nearest:', nearest)
#     print('distance: ', point.distance(nearest))
