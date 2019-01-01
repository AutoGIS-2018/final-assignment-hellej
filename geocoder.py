import utils.geocode as gc

print('\nStarting geocoder')

while True:
    print('\nWrite the search word or address to geocode...')
    search_word = input()
    
    if(len(search_word)==0):
        break
    
    coords = gc.geocode(search_word)
