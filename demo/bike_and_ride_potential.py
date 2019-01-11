
# Proof of concept:
# Analysis for bike & ride potential in Koskela, northern Helsinki

#%%
import pandas as pd
import geopandas as gpd
import utils.bike_ride_potential as br_pot
from fiona.crs import from_epsg
from datetime import datetime, timezone, timedelta

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
point_mask = pop_point.intersects(koskela_poly.loc[0, 'geometry'])
pop_koskela = pop_point.loc[point_mask]

#%%
pop_koskela.plot()
pop_koskela[:5].head(3)

#%%
test_point = pop_koskela[pop_koskela['INDEX'] == 17420].reset_index()
test_point.head()

#%% 
br_dfs = [br_pot.get_bike_ride_effect(row, dest_coords) for index, row in pop_koskela.iterrows()]
br_df = pd.concat(br_dfs)
print(br_df.head())

#%%
cols = ['hsy_idx', 'pop', 'tt', 'tt_diff', 'saved_min', 'b_distance', 'b_duration', 'last_p_str']
br_lines_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['arrow'], crs= from_epsg(4326))
br_lines_gdf.to_file('demo/output/br_lines.shp')

br_routes_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['bike_geom'], crs= from_epsg(4326))
br_routes_gdf.to_file('demo/output/br_routes.shp')

br_homes_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['first_point'], crs= from_epsg(4326))
br_homes_gdf.to_file('demo/output/br_homes.shp')

br_hubs_gdf = gpd.GeoDataFrame(data= br_df[cols], geometry= br_df['last_point'], crs= from_epsg(4326))
br_hubs_gdf.to_file('demo/output/br_hubs.shp')

#%%
grouped = br_hubs_gdf.groupby('last_p_str')
hub_dfs = []
for key, values in grouped:
    sum_pop = values['pop'].sum()
    sum_saved_tt = values['saved_min'].sum()
    avg_saving = sum_saved_tt / sum_pop
    hsy_idx = list(values['hsy_idx'])[0]
    geom = list(values['geometry'])[0]
    hub_gdf = gpd.GeoDataFrame(data={'hsy_idx': [hsy_idx], 'sum_pop': [sum_pop], 'avg_saving': [avg_saving]}, geometry= [geom], crs=from_epsg(4326))
    hub_dfs.append(hub_gdf)
hub_sum_gdf = pd.concat(hub_dfs)

#%%
hub_sum_gdf.to_file('demo/output/br_hubs_sums.shp')





#%%
#%%
# projected_hubs = br_hubs_gdf.to_crs(epsg=3879) 
# dests = list(projected_hubs['geometry'])
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
