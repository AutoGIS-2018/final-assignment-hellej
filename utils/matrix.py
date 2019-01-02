import pandas as pd
import geopandas as gpd
import itertools as itr

grid = gpd.read_file('data/MetropAccessGrid/MetropAccess_YKR_grid_EurefFIN.shp')

def targets_ykr_ids(targets, name):
    # reproject targets to grid CRS
    if (targets.crs != grid.crs):
        targets = targets.to_crs(grid.crs)

    # CRS should now match
    print('Extract YKR ids for targets...\nCRS match:', targets.crs == grid.crs)

    # join ykr grid info to targets
    targets_ykr = gpd.sjoin(targets, grid, how="inner", op="within")

    # gather target info to dictionary (ykr_id : name)
    target_info = {}
    for target in targets_ykr.itertuples(index=True, name='Pandas'):
        ykr_id = getattr(target, 'YKR_ID')
        target_info[ykr_id] = getattr(target, name)
    print('target info:', target_info)
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
        data = pd.read_csv(filepaths[ykr_id], sep=';')
        data = data[['from_id', 'to_id', 'pt_m_t']]
        tt_dfs[ykr_id] = data
    return tt_dfs

def get_target_permutations(tt_dfs):
    to_ids = tt_dfs.keys()
    print('Get all possible orders of targets...')
    to_ids_perms = list(itr.permutations(to_ids, len(to_ids)))
    print('found', len(to_ids_perms), 'permutations')
    return to_ids_perms

def get_all_ttimes(target_perms, tt_dfs):
    all_perm_times = []
    for target_perm in target_perms:
        perm_times = []
        for idx, target_id in enumerate(target_perm):
            if (idx > 0):
                from_id = target_perm[idx-1]
                target_df = tt_dfs[target_id]
                ttime = target_df.loc[target_df['from_id'] == from_id].iloc[0]['pt_m_t']
                perm_times.append(ttime)
        all_perm_times.append(perm_times)

    perms_times = pd.DataFrame(data={'perm': target_perms, 'ttimes': all_perm_times })
    return perms_times

def calculate_total_ttimes(perms_ttimes, target_info):
    perms_ttimes['first_id'] = [perm[0] for perm in perms_ttimes['perm']]
    perms_ttimes['first_name'] = [target_info[perm[0]] for perm in perms_ttimes['perm']]
    perms_ttimes['last_id'] = [perm[len(perm)-1] for perm in perms_ttimes['perm']]
    perms_ttimes['last_name'] = [target_info[perm[len(perm)-1]] for perm in perms_ttimes['perm']]
    perms_ttimes['tot_ttime'] = [sum(ttimes) for ttimes in perms_ttimes['ttimes']]
    # print(perms_ttimes.head(5))
    return perms_ttimes

def get_best_routes(all_ttimes_summary, origin, target):
    summary_df = all_ttimes_summary.copy()
    if (origin != ''):
        print('origin defined:', origin)
        summary_df = summary_df.loc[summary_df['first_name'] == origin]
    else:
        print('no origin defined...')
    if (target != ''):
        print('destination defined:', target)
        summary_df = summary_df.loc[summary_df['last_name'] == target]
    else:
        print('no destination defined...')
    
    # get min travel time
    min_tt = summary_df['tot_ttime'].min()
    # filter only routes having min travel time
    best_routes = summary_df.loc[summary_df['tot_ttime'] == min_tt]
    count_routes = len(best_routes.index)
    if (count_routes > 1):
        print('found multiple best routes ('+ str(count_routes) +')')
    elif (count_routes == 1):
        print('found one best route:')
    print(best_routes[['first_name', 'ttimes', 'last_name', 'tot_ttime']].head(5))
    return best_routes

def print_best_route_info(best_routes, target_info):
    route = best_routes.iloc[0]
    ykr_ids = route['perm']
    ttimes = route['ttimes']
    # print targets (and travel times) in best order
    for idx, ykr_id in enumerate(ykr_ids):
        name = target_info[ykr_id]
        minutes = ''
        if (idx > 0):
            minutes = ' ('+ str(ttimes[idx-1]) +' min)'
        print(str(idx+1)+'. '+ name + minutes)
    print('total travel time:', route['tot_ttime'], 'min')
