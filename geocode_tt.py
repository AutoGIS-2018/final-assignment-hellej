
# TEST GEOCODER
#%%
import geocode as gc

search_word = 'physicum'
coords = gc.geocode(search_word)
print(coords)


# GET TRAVEL TIMES
#%%
import geopandas as gpd
import matrix_utils as mu

#%%
cinemas = gpd.read_file('data/temp/cinemas.shp')
large_cinemas = cinemas.loc[cinemas['rooms'] > 2]
target_points = large_cinemas[:4]
print(target_points.head(5))

#%%
target_info = mu.targets_ykr_ids(target_points, 'name')

#%%
tt_dfs = mu.get_tt_between_targets(target_info, 'data/HelsinkiTravelTimeMatrix2018/')

#%%
target_perms = mu.get_target_permutations(tt_dfs)

#%%
perms_ttimes = mu.get_all_ttimes(target_perms, tt_dfs)

#%%
all_ttimes_summary = mu.calculate_total_ttimes(perms_ttimes, target_info)

#%%
best_routes = mu.get_best_routes(all_ttimes_summary, '', '')

#%%
mu.print_best_route_info(best_routes, target_info)

#%%
