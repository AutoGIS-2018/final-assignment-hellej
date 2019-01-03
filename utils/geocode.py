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

def geocodeInputs():
    print('\nStarting geocoder.')
    print('You can finish geocoding any time by typing "q" and pressing enter.')
    geocoded = []
    while True:
        print('\nWrite the search word or address to geocode or "q" to proceed: ', end='')
        search_word = input().lower()
        if(search_word == 'q'):
            break
        if(search_word == ''):
            continue
        result = geocode(search_word)
        while True:
            print('Are you happy with the geocoding result? y/n: ', end='')
            geocode_ok = input().lower()
            if(geocode_ok == 'y'):
                while True:
                    print('Give a short name for the place: ', end='')
                    name = input()
                    if (name == ''):
                        continue
                    result['name'] = name
                    geocoded.append(result)
                    break
                break
            elif(geocode_ok == 'n'):
                break
            else:
                continue
    return geocoded