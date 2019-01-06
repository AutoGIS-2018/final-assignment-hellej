import glob
import geopandas as gpd

def getUserInput(text, options, error):
    while True:
        print(text, end='')
        answer = input()
        if ('' not in options and answer == ''):
            continue
        if (len(options) > 1):
            loweroptions = [x.lower() for x in options]
            if (answer.lower() not in loweroptions):
                if (len(error) > 0):
                    print(error)
                continue
        return answer
