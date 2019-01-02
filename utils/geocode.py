import pandas as pd
import geopandas as gpd
import requests
import json
from urllib.parse import urlparse, urlencode
from shapely.geometry import Point
from fiona.crs import from_epsg
import glob

def getGeocodeRequest(search_word):
    # build request url for Digitransit Geocoding API 
    vars = {'text': search_word, 'size': 1}
    baseurl = 'https://api.digitransit.fi/geocoding/v1/search?'
    request = baseurl + urlencode(vars)
    return request

def geocode(search_word):
    # print('geocoding:', search_word)
    
    request = getGeocodeRequest(search_word)
    # print('request:', request)

    # execute API call
    georeq = requests.get(request)
    
    # print('JSON:', georeq.text)
    # parse result from json to python dictionary
    parsed_result = json.loads(georeq.text)
    
    # extract geocoded feature (GeoJSON)
    feat = parsed_result['features'][0]
    geom = feat['geometry']
    props = feat['properties']
    
    print('found:', props['label'])
    print('at:', geom['coordinates'])
    try:
        print('from neighbourhood:', props['neighbourhood'])
    except:
        pass
    print('with confidence:', round(props['confidence'],2))
    
    return {'coords': geom['coordinates'], 'place': props['label'], 'confidence': round(props['confidence'],3), 'search_word': search_word}

def geoCodedToGeoDF(geocode_results):
    names = []
    addresses = []
    points = []
    for geocoded in geocode_results:
        names.append(geocoded['name'])
        points.append(Point(geocoded['coords']))
        addresses.append(geocoded['search_word'])
    geodf = gpd.GeoDataFrame(data={'name': names, 'address': addresses, 'geometry': points}, crs=from_epsg(4326))
    print('\nGeocoded:')
    print(geodf)
    return geodf

def loadInputShapefiles():
    shapefiles = glob.glob('input/*.shp')
    if (len(shapefiles) > 0):
        print('\nExisting locations (.shp) in the foldedr:')
        for idx, shapefile in enumerate(shapefiles):
            print(' ['+ str(idx+1) +']: '+ shapefile)
        print('Do you want to import one of the above files? y/n: ', end='')
        b_import_file = input().lower()
        if (b_import_file == 'y'):
            while True:
                print('specify file number to import (1,2,3...): ', end='')
                file_num = int(input())
                try:
                    file_path = shapefiles[file_num-1]
                    read_file = gpd.read_file(file_path)
                    print('successfully loaded file:')
                    print(read_file)
                    return read_file
                except:
                    print('invalid number...')
                    continue

def saveToFile(targetGeom):
    while True:
        print('\nSpecify a file for saving the locations: ', end='')
        filename = input()
        if (filename == ''):
            continue
        targetGeom.to_file('input/'+filename+'.shp')
        break
