import requests
import json
import polyline
from shapely.geometry import Point, LineString

def build_plan_query(coords_from, coords_to, walkSpeed, maxWalkDistance):
    return f'''
    plan(
        from: {{lat: {coords_from['lat']}, lon: {coords_from['lon']}}}
        to: {{lat: {coords_to['lat']}, lon: {coords_to['lon']}}}
        numItineraries: 3,
        walkSpeed: {walkSpeed},
        maxWalkDistance: {maxWalkDistance}
    )
    '''

def build_full_route_query(coords_from, coords_to, walkSpeed, maxWalkDistance):
    query = f'''
    {{
    {build_plan_query(coords_from, coords_to, walkSpeed, maxWalkDistance)}
    {{
        itineraries {{
            duration
            legs {{
                mode
                duration
                distance
                transitLeg
                legGeometry {{
                    length
                    points
                }}
            }}
        }}
    }}
    }}
    '''
    return query

def build_travel_time_query(coords_from, coords_to, walkSpeed, maxWalkDistance):
    query = f'''
    {{
    {build_plan_query(coords_from, coords_to, walkSpeed, maxWalkDistance)}
    {{ itineraries {{ duration }} }}
    }}
    '''
    return query

def run_query(query):
    dt_routing_endpoint = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql' 
    headers = {'Content-Type': 'application/json'}
    request = requests.post(dt_routing_endpoint, json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed to run by returning code of {}. {}'.format(request.status_code, query))

def get_route_itineraries(coords_from, coords_to, walkSpeed, maxWalkDistance):
    query = build_full_route_query(coords_from, coords_to, walkSpeed, maxWalkDistance)
    response = run_query(query)
    itineraries = response['data']['plan']['itineraries']
    return itineraries

def create_line_geom(point_coords):
    try:
        return LineString([point for point in point_coords])
    except:
        return

def parse_route_geom(itins):
    for itin in itins:
        itin_coords = []
        legs = itin['legs']
        for leg in legs:
            geom = leg['legGeometry']['points']
            # parse coordinates from Google Encoded Polyline Algorithm Format
            coords = polyline.decode(geom)
            leg['line_geom'] = create_line_geom(coords)
            itin_coords += coords
        itin['line_geom'] = create_line_geom(itin_coords)
    return itins

def get_mean_travel_time(coords_from, coords_to, walkSpeed, maxWalkDistance):
    query = build_travel_time_query(coords_from, coords_to, walkSpeed, maxWalkDistance)
    response = run_query(query)
    itineraries = response['data']['plan']['itineraries']
    # calculate mean travel time of three inireraries
    duration_sum = 0
    for itin in itineraries:
        duration_sum += itin['duration']
    mean_tt_min = int(round((duration_sum/len(itineraries))/60))
    return mean_tt_min
