import glob
import geopandas as gpd
from datetime import datetime, date, time, timedelta

def get_user_input(text, options, caseSens, error):
    while True:
        print(text, end='')
        answer = input()
        if (answer == '' and '' not in options):
            continue
        if (len(options) > 1):
            if (caseSens == True):
                if(answer not in options):
                    if (len(error) > 0):
                        print(error)
                    continue
            loweroptions = [x.lower() for x in options]
            if (answer.lower() not in loweroptions):
                if (len(error) > 0):
                    print(error)
                continue
        return answer

def get_next_weekday():
    weekday = datetime.weekday(date.today())
    skipdays = 1
    if (weekday == 4):
        skipdays = 3
    if (weekday == 5):
        skipdays = 2
    next_weekday = date.today() + timedelta(days=skipdays)
    return next_weekday

def get_next_weekday_datetime(hh, mm):
    next_weekday_datetime = datetime.combine(get_next_weekday(), time(hh, mm))
    return next_weekday_datetime
