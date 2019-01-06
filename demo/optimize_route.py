
# MULTI STOP ROUTE OPTIMIZATION DEMO

#%%
import geopandas as gpd
import utils.travel_times as tts
import utils.routes_tt as rtts

digitransit = False

#%%
# read and filter test data (cinemas as stops)
cinemas = gpd.read_file('data/temp/cinemas.shp')
large_cinemas = cinemas.loc[cinemas['rooms'] > 2]
target_points = large_cinemas[:3]

#%%
# get and gather target_info (ykr_ids, names & addresses)
target_info = tts.gather_target_info(target_points, 'name', 'address_y', digitransit)
print(target_info)

#%%
# read and gather only relevant travel time dataframes to a dictionary
tts_dict = tts.get_tt_between_targets(target_info, 'data/HelsinkiTravelTimeMatrix2018/', digitransit)

#%%
# find and collect all possible route options
target_perms = rtts.get_target_permutations(tts_dict)

#%%
# extract and collect travel times between stops for all route options
perms_ttimes = rtts.get_all_ttimes(target_perms, tts_dict)

#%%
# calculate total travel times for all route options
all_ttimes_summary = rtts.calculate_total_ttimes(perms_ttimes, target_info)

#%%
# get best routes from all route options by minimizing total travel time
best_routes = rtts.get_best_routes(all_ttimes_summary, '', '')

#%%
# print 8 best routes
rtts.print_best_route_info(best_routes, target_info)

#%%
