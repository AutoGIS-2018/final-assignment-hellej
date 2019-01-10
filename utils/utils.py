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
