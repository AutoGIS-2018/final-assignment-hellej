import utils.geocode as gc

def geocodeInputs():
    print('\nStarting geocoder.')
    print('You can finish geocoding any time by typing "q" and pressing enter.')

    geocoded = []

    while True:
        print('\nWrite the search word or address to geocode or "q" to proceed: ', end='')
        search_word = input().lower()
        if(search_word == 'q'):
            break
        if(search_word == ''):
            continue
        
        result = gc.geocode(search_word)

        while True:
            print('Are you happy with the geocoding result? y/n: ', end='')
            geocode_ok = input().lower()

            if(geocode_ok == 'y'):
                while True:
                    print('Give a short name for the place: ', end='')
                    name = input()
                    if (name == ''):
                        continue
                    result['name'] = name
                    geocoded.append(result)
                    break
                break
            elif(geocode_ok == 'n'):
                break
            else:
                continue
    return geocoded
