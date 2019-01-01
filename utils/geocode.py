import requests
import json
from urllib.parse import urlparse, urlencode

def getGeocodeRequest(search_word):
    # build request url for Digitransit Geocoding API 
    vars = {'text': search_word, 'size': 1}
    baseurl = 'https://api.digitransit.fi/geocoding/v1/search?'
    request = baseurl + urlencode(vars)
    return request

def geocode(search_word):
    print('\nGeocoding:', search_word)
    
    request = getGeocodeRequest(search_word)
    print('request:', request)

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
    print('from neighbourhood:', props['neighbourhood'])
    print('with confidence:', props['confidence'])
    
    return geom['coordinates']
