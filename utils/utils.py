import glob
import geopandas as gpd
from datetime import datetime, date, time, timedelta

def get_user_input(text, options, caseSens, error):
    '''
    Function for asking and reading user input from keyboard. 
    User is asked the question (text: string) until the input satisfies
    the requirements for the answer (options: [] & caseSens: bool).
    If user input is not valid, error message is shown (and question asked again).
    Returns
    -------
    <string>
        Read user input as string.
    '''
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
