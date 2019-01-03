import glob
import geopandas as gpd

def saveToShapefile(targetGeom, folder):
    while True:
        print('\nSpecify a file name for saving the locations: ', end='')
        filename = input()
        if (filename == ''):
            continue
        targetGeom.to_file(folder+filename+'.shp')
        break

def loadInputShapefile(folder):
    shapefiles = glob.glob(folder+'*.shp')
    if (len(shapefiles) > 0):
        print('\nExisting locations (.shp) in the foldedr:')
        for idx, shapefile in enumerate(shapefiles):
            print(' ['+ str(idx+1) +']: '+ shapefile)
        while True:
            print('Do you want to import one of the above files? y/n: ', end='')
            b_import_file = input().lower()
            if (b_import_file == 'y'):
                while True:
                    print('specify file number to import (1,2,3...): ', end='')
                    file_num = int(input())
                    try:
                        file_path = shapefiles[file_num-1]
                        read_file = gpd.read_file(file_path)
                        print('\nSuccessfully loaded locations:')
                        print(read_file[['name', 'address']])
                        return read_file
                    except:
                        print('invalid number...')
                        continue
            if (b_import_file == 'n'):
                break
            else:
                continue
