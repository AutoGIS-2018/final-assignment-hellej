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

def get_filepath_to_tt_file(ykr_id, folder):
    subfolder = str(ykr_id)[:4]+'xxx/'
    filename = 'travel_times_to_ '+ str(ykr_id) +'.txt'
    file_path = folder + subfolder + filename
    return file_path

def get_tt_between_targets(target_info, folder, b_realtime):
    ykr_ids = target_info.keys()
    tts = {}
    for to_id in ykr_ids:
        if (b_realtime == True):
            print('IMPLEMENT REALTIME')
        if (b_realtime == False):
            try:
                filepath = get_filepath_to_tt_file(to_id, folder)
                tts_df = pd.read_csv(filepath, sep=';')
                to_tts = {}
                for from_id in ykr_ids:
                    from_tt = tts_df.loc[tts_df['from_id'] == from_id].iloc[0]['pt_m_t']
                    to_tts[from_id] = from_tt
                tts[to_id] = to_tts
            except:
                print('\nError: no travel time file found for: '+ (target_info[to_id]['name'])+'.\n')
                return
    return tts
