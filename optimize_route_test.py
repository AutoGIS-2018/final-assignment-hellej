
# TEST GEOCODER
#%%
import utils.geocode as gc

#%%
search_word = 'physicum'
coords = gc.geocode(search_word)


# GET TRAVEL TIMES
#%%
import geopandas as gpd
import utils.matrix as mtrx
import utils.routes_tt as rtts

#%%
cinemas = gpd.read_file('data/temp/cinemas.shp')
large_cinemas = cinemas.loc[cinemas['rooms'] > 2]
target_points = large_cinemas[:4]

#%%
target_info = mtrx.targets_ykr_ids(target_points, 'name')

#%%
tt_dfs = mtrx.get_tt_between_targets(target_info, 'data/HelsinkiTravelTimeMatrix2018/')

#%%
target_perms = rtts.get_target_permutations(tt_dfs)

#%%
perms_ttimes = rtts.get_all_ttimes(target_perms, tt_dfs)

#%%
all_ttimes_summary = rtts.calculate_total_ttimes(perms_ttimes, target_info)

#%%
best_routes = rtts.get_best_routes(all_ttimes_summary, '', '')

#%%
rtts.print_best_route_info(best_routes, target_info)

#%%
