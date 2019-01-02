import geocoder as gc
import utils.geocode as geocode

geocoded = gc.geocodeInputs()

if (len(geocoded) > 0):
    targetGeom = geocode.geoCodedToGeoDF(geocoded)
    print('\nFinished geocoding.\n')
