
# GEOCODING DEMO

#%%
import utils.dt_geocode as gc

#%%
search_word = 'physicum'
# geocode with search_word using Digitransit Geocoding API
gc_results = gc.geocode(search_word)

#%%
# print geocoding result dictionary
print(gc_results)

#%%
