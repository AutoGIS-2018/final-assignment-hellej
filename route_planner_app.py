import geocoder as gc
import utils.geocode as geocode
import utils.matrix as mtrx
import utils.routes_tt as rtts

targetGeom = geocode.loadInputShapefiles()

if(targetGeom is None):
    geocoded = gc.geocodeInputs()
    if (len(geocoded) > 0):
        targetGeom = geocode.geoCodedToGeoDF(geocoded)
        geocode.saveToFile(targetGeom)
    print('\nFinished geocoding.\n')

if(len(targetGeom.index) > 0):
    target_info = mtrx.targets_ykr_ids(targetGeom, 'name')
    tt_dfs = mtrx.get_tt_between_targets(target_info, 'data/HelsinkiTravelTimeMatrix2018/')
    target_perms = rtts.get_target_permutations(tt_dfs)
    perms_ttimes = rtts.get_all_ttimes(target_perms, tt_dfs)
    all_ttimes_summary = rtts.calculate_total_ttimes(perms_ttimes, target_info)
    best_routes = rtts.get_best_routes(all_ttimes_summary, '', '')
    rtts.print_best_route_info(best_routes, target_info)
