import utils.dt_geocode as gc
import utils.travel_times as tts
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
    target_info = tts.gather_target_info(targetGeom, 'name', 'address', False)
    if (target_info is not None):
        tts_dict = tts.get_tt_between_targets(target_info, 'data/HelsinkiTravelTimeMatrix2018/', False)
        if(tts_dict is not None):
            target_perms = rtts.get_target_permutations(tts_dict)
            perms_ttimes = rtts.get_all_ttimes(target_perms, tts_dict)
            all_ttimes_summary = rtts.calculate_total_ttimes(perms_ttimes, target_info)
            route_params = rtts.askOrigDest(target_info)
            best_routes = rtts.get_best_routes(all_ttimes_summary, route_params['orig'], route_params['dest'])
            rtts.print_best_route_info(best_routes, target_info)
