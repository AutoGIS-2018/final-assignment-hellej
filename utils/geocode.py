import pandas as pd
import geopandas as gpd
import requests
import json
from urllib.parse import urlparse, urlencode
from shapely.geometry import Point
from fiona.crs import from_epsg

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
