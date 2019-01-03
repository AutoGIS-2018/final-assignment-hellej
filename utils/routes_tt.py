import itertools as itr
import pandas as pd

def get_target_permutations(tt_dfs):
    to_ids = tt_dfs.keys()
    print('\nGet all possible routes...')
    to_ids_perms = list(itr.permutations(to_ids, len(to_ids)))
    print('found', len(to_ids_perms), 'route options')
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
    perms_ttimes['orig_id'] = [perm[0] for perm in perms_ttimes['perm']]
    perms_ttimes['orig_name'] = [target_info[perm[0]]['name'] for perm in perms_ttimes['perm']]
    perms_ttimes['dest_id'] = [perm[len(perm)-1] for perm in perms_ttimes['perm']]
    perms_ttimes['dest_name'] = [target_info[perm[len(perm)-1]]['name'] for perm in perms_ttimes['perm']]
    perms_ttimes['tot_ttime'] = [sum(ttimes) for ttimes in perms_ttimes['ttimes']]
    return perms_ttimes

def get_best_routes(all_ttimes_summary, origin, target):
    summary_df = all_ttimes_summary.copy()
    if (origin != ''):
        print('origin defined:', origin)
        summary_df = summary_df.loc[summary_df['orig_name'] == origin]
    else:
        print('no origin defined...')
    if (target != ''):
        print('destination defined:', target)
        summary_df = summary_df.loc[summary_df['dest_name'] == target]
    else:
        print('no destination defined...')
    # order routes by total travel time
    best_routes = summary_df.sort_values(by='tot_ttime', ascending=True).reset_index(drop=True)
    return best_routes

def print_route(route, target_info, idx):
    ykr_ids = route['perm']
    ttimes = route['ttimes']
    # print targets (and travel times) in best order
    print(str(idx+1) +'. route: '+ str(route['tot_ttime']) +' min:')
    for idx, ykr_id in enumerate(ykr_ids):
        name = target_info[ykr_id]['name']
        address = target_info[ykr_id]['address']
        minutes = ''
        if (idx > 0):
            minutes = ' ('+ str(ttimes[idx-1]) +' min)'
        print(' '+str(idx+1)+'. '+ name +': '+ address + minutes)

def print_best_route_info(best_routes, target_info):
    # get min travel time
    min_tt = best_routes['tot_ttime'].min()
    # count foutes having minimum travel time
    count_best_routes = len(best_routes.loc[best_routes['tot_ttime'] == min_tt].index)
    if (count_best_routes > 1):
        print('\nFound multiple best routes ('+ str(count_best_routes) +'):')
    elif (count_best_routes == 1):
        print('\nFound following best routes:')
    for idx, route in best_routes[:8].iterrows():
        print_route(route, target_info, idx)
    print('\n')
