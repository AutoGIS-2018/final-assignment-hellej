from functools import reduce
import glob
import utils.dt_geocode as gc
import utils.travel_times as tts
import utils.routes_tt as rtts
import utils.utils as utils
import geopandas as gpd

targetGeom = None

# list existing shapefiles and ask if one of them should be imported
shp_list = glob.glob('input/*.shp')
if (len(shp_list) > 0):
    print('\nExisting locations (.shp) in the foldedr:')
    shape_nums = []
    for idx, shapefile in enumerate(shp_list):
        # print names and indexes of found shapefiles
        print(' ['+ str(idx+1) +']: '+ shapefile)
        shape_nums.append(str(idx+1))
    b_import_file = utils.getUserInput('Do you want to import one of the above files? y/n: ', ['y', 'n'], False, '').lower()
    # prodeed to importing file
    if (b_import_file == 'y'):
        # ask which file (index) should be imported
        file_num = int(utils.getUserInput('Specify file number to import '+ str(shape_nums) +': ', shape_nums, False, 'Invalid number'))
        # read file
        targetGeom = gpd.read_file(shp_list[file_num-1])
        print('\nSuccessfully loaded locations:')
        print(targetGeom[['name', 'address']])

# ask and geocode inputs if shapefile was not imported
if(targetGeom is None):
    print('\nStarting geocoder.')
    geocoded = []
    while True:
        print('\nWrite the search word or address to geocode or "q" to proceed: ', end='')
        search_word = input().lower()
        if(search_word == 'q'):
            break
        if(search_word == ''):
            continue
        result = gc.geocode(search_word)
        b_geocode_ok = utils.getUserInput('Are you happy with the geocoding result? y/n: ', ['y', 'n'], False, '').lower()
        if(b_geocode_ok == 'y'):
            while True:
                print('Give a short name for the place: ', end='')
                name = input()
                if (name == ''):
                    continue
                result['name'] = name
                geocoded.append(result)
                break
            continue
        elif(b_geocode_ok == 'n'):
            continue
    # export geocoded locations to shapefile (if any)
    if (len(geocoded) > 0):
        # create pandas data frame from geocoded locations (list of dictionaries)
        targetGeom = gc.geoCodedToGeoDF(geocoded)
        filename = utils.getUserInput('\nSpecify a file name for saving the locations: ', [], False, '')
        targetGeom.to_file('input/'+filename+'.shp')
        print('\nFinished geocoding.')

# proceed to route optimization if length of target geometries is more than 1
if(len(targetGeom.index) > 1):
    # ask wether travel time matrix or Digitransit API should be usod to obtain travel time information
    matrix_or_digitransit = utils.getUserInput('\nDo you want to extract travel times from travel time matrix or Digitransit API? "matrix"/"digitransit": ', ['matrix', 'digitransit'], False, '').lower()
    digitransit = True if matrix_or_digitransit == 'digitransit' else False
    # gather and get target info as dictionary
    target_info = tts.gather_target_info(targetGeom, 'name', 'address', digitransit)
    if (target_info is not None):
        # collect and get all travel times between targets as dictionary
        tts_dict = tts.get_tt_between_targets(target_info, 'data/HelsinkiTravelTimeMatrix2018/', digitransit)
        if(tts_dict is not None):
            # get all possible stop sequences (route options)
            target_perms = rtts.get_target_permutations(tts_dict)
            # get travel times for all stop sequences (route options)
            perms_ttimes = rtts.get_all_ttimes(target_perms, tts_dict)
            # add total travel times to all route options
            all_ttimes_summary = rtts.calculate_total_ttimes(perms_ttimes, target_info)
            # ask if user wants to define fixed origin and/or destination stop
            print('\nSelect origin and destination from ', end='')
            stopnames = [target['name'] for target in target_info.values()]
            print(stopnames)
            origin = utils.getUserInput('type origin name (or leave empty): ', stopnames + [''], True, 'invalid stop name')
            destination = utils.getUserInput('type destination name (or leave empty): ', stopnames + [''], True, 'invalid stop name')
            # get best routes based on shortest total travel times
            best_routes = rtts.get_best_routes(all_ttimes_summary, origin, destination)
            rtts.print_best_route_info(best_routes, target_info)
else:
    print('\nNot enough stops speficied.')
