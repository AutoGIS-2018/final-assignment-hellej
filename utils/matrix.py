import pandas as pd
import geopandas as gpd

grid = gpd.read_file('data/MetropAccessGrid/MetropAccess_YKR_grid_EurefFIN.shp')

def targets_ykr_ids(targets, name, address):
    # reproject targets to grid CRS
    if (targets.crs != grid.crs):
        targets = targets.to_crs(grid.crs)
    # CRS should now match
    print('\nExtract YKR ids for targets...\nCRS match:', targets.crs == grid.crs)
    # join ykr grid info to targets
    targets_ykr = gpd.sjoin(targets, grid, how="inner", op="within")
    target_names = list(targets['name'])
    target_ykr_names = list(targets_ykr['name'])
    # check if YKR ids were found for all targets
    if(len(target_ykr_names) < len(target_names)):
        # get and print targets without YKR ids if any
        missing = list(set(target_names)-set(target_ykr_names))
        print('\nError: targets '+ str(missing)+' are outside YKR area.\n')
        return
    # gather target info to a dictionary (ykr_id : name)
    target_info = {}
    for target in targets_ykr.itertuples(index=True, name='Pandas'):
        ykr_id = getattr(target, 'YKR_ID')
        target_info[ykr_id] = {'name': getattr(target, name), 'address': getattr(target, address)}
    return target_info

def get_filepaths_to_tt_files(ykr_ids, folder):
    filepaths = {}
    for ykr_id in ykr_ids:
        subfolder = str(ykr_id)[:4]+'xxx/'
        filename = 'travel_times_to_ '+ str(ykr_id) +'.txt'
        path = folder + subfolder + filename
        filepaths[ykr_id] = path
    return filepaths

def get_tt_between_targets(target_info, folder):
    filepaths = get_filepaths_to_tt_files(target_info.keys(), folder)
    tt_dfs = {}
    for ykr_id in filepaths:
        try:
            data = pd.read_csv(filepaths[ykr_id], sep=';')
            data = data[['from_id', 'to_id', 'pt_m_t']]
            tt_dfs[ykr_id] = data
        except:
            print('\nError: no travel time file found for: '+ (target_info[ykr_id]['name'])+'.\n')
            return
    return tt_dfs
