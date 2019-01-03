```
(geoenv) Jooses-MBP:final-assignment-hellej joose$ python route_planner_app.py 

Existing locations (.shp) in the foldedr:
 [1]: input/stadissa.shp
 [2]: input/serkut.shp
Do you want to import one of the above files? y/n: y
specify file number to import (1,2,3...): 2

Successfully loaded locations:
      name                address
0  Koskela  juhana herttuan tie 3
1     Ellu      ruukinlahdentie 3
2    Ville        kolmas linja 14
3     Okko   itäinen alppirinne 1
4     Iitu      teollisuuskatu 18

Extract YKR ids for targets...
CRS match: True

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
