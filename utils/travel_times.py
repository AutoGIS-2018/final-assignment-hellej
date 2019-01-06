import pandas as pd
import geopandas as gpd
import utils.dt_routing as dt_rt
from fiona.crs import from_epsg
import sys

grid = gpd.read_file('data/MetropAccessGrid/MetropAccess_YKR_grid_EurefFIN.shp')

def add_ykr_ids_to_targets(targets):
    # reproject targets to grid CRS
    if (targets.crs != grid.crs):
        targets = targets.to_crs(grid.crs)
    # CRS should now match
    print('\nExtract YKR ids for targets...\nCRS match:', targets.crs == grid.crs)
    # join ykr grid info to targets
    targets_ids = gpd.sjoin(targets, grid, how="inner", op="within")
    target_names = list(targets['name'])
    target_ids_names = list(targets_ids['name'])
    # check if YKR ids were found for all targets
    if(len(target_ids_names) < len(target_names)):
        # get and print targets without YKR ids if any
        missing = list(set(target_names)-set(target_ids_names))
        print('\nError: targets '+ str(missing)+' are outside YKR area.\n')
        return
    return targets_ids

def gather_target_info(targets, name, address, digitransit):
    if (digitransit == True):
        id_col = 'ROW_ID'
        targets['ROW_ID'] = targets.reset_index().index
    else:
        id_col = 'YKR_ID'
        targets = add_ykr_ids_to_targets(targets)
        if (targets is None):
            return

    # gather target info to a dictionary (ykr_id : name)
    targets = targets.to_crs(from_epsg(4326))
    target_info = {}
    for target in targets.itertuples(index=True, name='Pandas'):
        target_id = getattr(target, id_col)
        point = getattr(target, 'geometry')
        latLon = { 'lat': round(point.y, 4), 'lon': round(point.x, 4) }
        target_info[target_id] = {'name': getattr(target, name), 'address': getattr(target, address), 'latLon': latLon}
    return target_info

def get_filepath_to_tt_file(ykr_id, folder):
    subfolder = str(ykr_id)[:4]+'xxx/'
    filename = 'travel_times_to_ '+ str(ykr_id) +'.txt'
    file_path = folder + subfolder + filename
    return file_path

def get_tt_between_targets(target_info, folder, digitransit):
    target_ids = target_info.keys()
    tts = {}
    sys.stdout.write('querying travel times to targets: ')
    sys.stdout.flush()
    for idx, to_id in enumerate(target_ids):
        if (digitransit == True):
            sys.stdout.write(str(idx+1)+'/'+str(len(target_ids))+' ')
            sys.stdout.flush()
            try:
                to_tts = {}
                for from_id in target_ids:
                    walkSpeed = '1.33'
                    if (from_id != to_id):
                        from_tt = dt_rt.get_mean_travel_time(target_info[from_id]['latLon'], target_info[to_id]['latLon'], walkSpeed, 6000)
                        to_tts[from_id] = from_tt
                tts[to_id] = to_tts
            except:
                print('\nError: no travel time file found for: '+ (target_info[to_id]['name'])+'.\n')
                return
        if (digitransit == False):
            try:
                filepath = get_filepath_to_tt_file(to_id, folder)
                tts_df = pd.read_csv(filepath, sep=';')
                to_tts = {}
                for from_id in target_ids:
                    from_tt = tts_df.loc[tts_df['from_id'] == from_id].iloc[0]['pt_m_t']
                    to_tts[from_id] = from_tt
                tts[to_id] = to_tts
            except:
                print('\nError: no travel time file found for: '+ (target_info[to_id]['name'])+'.\n')
                return
    return tts
