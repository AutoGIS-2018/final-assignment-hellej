import geopandas as gpd

grid = gpd.read_file('data/MetropAccessGrid/MetropAccess_YKR_grid_EurefFIN.shp')

def targets_ykr_ids(targets):    
    # print column names
    # print('grid cols: ', grid.columns)
    # print('targets cols: ', targets.columns)
    
    # check if CRS of layers match (-> False)
    # print('CRS match:', targets.crs == grid.crs)
    
    # reproject targets to grid CRS
    targets = targets.to_crs(grid.crs)
    # CRS should now match
    print('CRS match:', targets.crs == grid.crs)
    
    # join ykr grid info to targets
    targets_ykr = gpd.sjoin(targets, grid, how="inner", op="within")
    # get the ids as list
    ykr_ids = targets_ykr.YKR_ID.tolist()
    
    timecols = []
    names = []
    for idx, target in targets.iterrows():
        columnn = 'pt_r_t_'+str(idx)
        # print('target:', target)
        names.append(target['name'])
        timecols.append(columnn)
        
    return {'ykr_ids': ykr_ids, 'timecols': timecols, 'names': names}