import utils.dt_geocode as gc
import utils.matrix as mtrx
import utils.routes_tt as rtts
import utils.utils as utils

targetGeom = utils.loadInputShapefile('input/')

if(targetGeom is None):
    geocoded = gc.geocodeInputs()
    if (len(geocoded) > 0):
        targetGeom = gc.geoCodedToGeoDF(geocoded)
        utils.saveToShapefile(targetGeom, 'input/')
    print('\nFinished geocoding.')

if(len(targetGeom.index) > 0):
    target_info = mtrx.targets_ykr_ids(targetGeom, 'name', 'address')
    tt_dfs = mtrx.get_tt_between_targets(target_info, 'data/HelsinkiTravelTimeMatrix2018/')
    target_perms = rtts.get_target_permutations(tt_dfs)
    perms_ttimes = rtts.get_all_ttimes(target_perms, tt_dfs)
    all_ttimes_summary = rtts.calculate_total_ttimes(perms_ttimes, target_info)
    route_params = rtts.askOrigDest(target_info)
    best_routes = rtts.get_best_routes(all_ttimes_summary, route_params['orig'], route_params['dest'])
    rtts.print_best_route_info(best_routes, target_info)
