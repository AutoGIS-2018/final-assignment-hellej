## With geocoding
```
(geoenv) Jooses-MacBook-Pro:final-assignment-hellej joose$ python route_planner_app.py 

Existing locations (.shp) in the foldedr:
 [1]: input/stadissa.shp
 [2]: input/outside.shp
 [3]: input/serkut.shp
Do you want to import one of the above files? y/n: n

Starting geocoder.

Write the search word or address to geocode or "q" to proceed: juhana herttuan tie 3
found: Juhana Herttuan tie 3, Helsinki
at: [24.969732, 60.217748]
from neighbourhood: Koskela
with confidence: 1
Are you happy with the geocoding result? y/n: y
Give a short name for the place: Koskela

Write the search word or address to geocode or "q" to proceed: ruukinlahdentie 3
found: Ruukinlahdentie 3, Helsinki
at: [24.872825, 60.16198]
from neighbourhood: Myllykallio
with confidence: 1
Are you happy with the geocoding result? y/n: y
Give a short name for the place: Ellu

Write the search word or address to geocode or "q" to proceed: kolmas linja 14
found: Kolmas linja 14, Helsinki
at: [24.948377, 60.182609]
from neighbourhood: Linjat
with confidence: 1
Are you happy with the geocoding result? y/n: y
Give a short name for the place: Ville

Write the search word or address to geocode or "q" to proceed: itäinen alppirinne 1
found: Itäinen Alppirinne 1a, Helsinki
at: [24.950168, 60.185841]
from neighbourhood: Linjat
with confidence: 0.99
Are you happy with the geocoding result? y/n: y
Give a short name for the place: Okko

Write the search word or address to geocode or "q" to proceed: teollisuuskatu 18
found: Teollisuuskatu 18, Helsinki
at: [24.944845, 60.194894]
from neighbourhood: Vallila
with confidence: 1
Are you happy with the geocoding result? y/n: y
Give a short name for the place: Iitu

Write the search word or address to geocode or "q" to proceed: q

Geocoded:
      name                address                     geometry
0  Koskela  juhana herttuan tie 3  POINT (24.969732 60.217748)
1     Ellu      ruukinlahdentie 3   POINT (24.872825 60.16198)
2    Ville        kolmas linja 14  POINT (24.948377 60.182609)
3     Okko   itäinen alppirinne 1  POINT (24.950168 60.185841)
4     Iitu      teollisuuskatu 18  POINT (24.944845 60.194894)

Specify a file name for saving the locations: serkut

Finished geocoding.

Do you want to extract travel times from travel time matrix or Digitransit API? "matrix"/"digitransit": matrix

Extract YKR ids for targets...
CRS match: True
querying travel times to targets: 1/5 2/5 3/5 4/5 5/5 
Get all possible routes...
found 120 route options

Select origin and destination from ['Koskela', 'Ellu', 'Ville', 'Okko', 'Iitu']
type origin name (or leave empty): 
type destination name (or leave empty): Ville

Found the following best routes:
Route 1: 90 min:
  1. Ellu: ruukinlahdentie 3
  2. Okko: itäinen alppirinne 1 (28 min)
  3. Iitu: teollisuuskatu 18 (8 min)
  4. Koskela: juhana herttuan tie 3 (23 min)
  5. Ville: kolmas linja 14 (31 min)
Route 2: 92 min:
  1. Ellu: ruukinlahdentie 3
  2. Koskela: juhana herttuan tie 3 (46 min)
  3. Iitu: teollisuuskatu 18 (30 min)
  4. Okko: itäinen alppirinne 1 (9 min)
  5. Ville: kolmas linja 14 (7 min)
Route 3: 94 min:
  1. Koskela: juhana herttuan tie 3
  2. Iitu: teollisuuskatu 18 (30 min)
  3. Okko: itäinen alppirinne 1 (9 min)
  4. Ellu: ruukinlahdentie 3 (28 min)
  5. Ville: kolmas linja 14 (27 min)
Route 4: 96 min:
  1. Ellu: ruukinlahdentie 3
  2. Iitu: teollisuuskatu 18 (35 min)
  3. Koskela: juhana herttuan tie 3 (23 min)
  4. Okko: itäinen alppirinne 1 (31 min)
  5. Ville: kolmas linja 14 (7 min)
```

## With locations imported from a shapefile
```
(geoenv) Jooses-MacBook-Pro:final-assignment-hellej joose$ python route_planner_app.py 

Existing locations (.shp) in the foldedr:
 [1]: input/stadissa.shp
 [2]: input/outside.shp
 [3]: input/serkut.shp
Do you want to import one of the above files? y/n: y
Specify file number to import ['1', '2', '3']: 3

Successfully loaded locations:
      name                address
0  Koskela  juhana herttuan tie 3
1     Ellu      ruukinlahdentie 3
2    Ville        kolmas linja 14
3     Okko   itäinen alppirinne 1
4     Iitu      teollisuuskatu 18

Do you want to extract travel times from travel time matrix or Digitransit API? "matrix"/"digitransit": matrix

Extract YKR ids for targets...
CRS match: True
querying travel times to targets: 1/5 2/5 3/5 4/5 5/5
Get all possible routes...
found 120 route options

Select origin and destination from ['Koskela', 'Ellu', 'Ville', 'Okko', 'Iitu']
type origin name (or leave empty): 
type destination name (or leave empty): Ville

Found the following best routes:
Route 1: 90 min:
  1. Ellu: ruukinlahdentie 3
  2. Okko: itäinen alppirinne 1 (28 min)
  3. Iitu: teollisuuskatu 18 (8 min)
  4. Koskela: juhana herttuan tie 3 (23 min)
  5. Ville: kolmas linja 14 (31 min)
Route 2: 92 min:
  1. Ellu: ruukinlahdentie 3
  2. Koskela: juhana herttuan tie 3 (46 min)
  3. Iitu: teollisuuskatu 18 (30 min)
  4. Okko: itäinen alppirinne 1 (9 min)
  5. Ville: kolmas linja 14 (7 min)
Route 3: 94 min:
  1. Koskela: juhana herttuan tie 3
  2. Iitu: teollisuuskatu 18 (30 min)
  3. Okko: itäinen alppirinne 1 (9 min)
  4. Ellu: ruukinlahdentie 3 (28 min)
  5. Ville: kolmas linja 14 (27 min)
Route 4: 96 min:
  1. Ellu: ruukinlahdentie 3
  2. Iitu: teollisuuskatu 18 (35 min)
  3. Koskela: juhana herttuan tie 3 (23 min)
  4. Okko: itäinen alppirinne 1 (31 min)
  5. Ville: kolmas linja 14 (7 min)
```
