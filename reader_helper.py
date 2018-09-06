import pandas as pd

def ReadingTheScalarDataFile(filename):
    print('Reading the data file : ', filename)
    datafile = open(filename,'r+')
    filereader = datafile.readlines()
    datafile.close()
    scalar_badflag = ''
    for val in ((filereader[4][:-1]).split(": "))[1]:
        if val != ' ':
            scalar_badflag += val
    longitudes = ((filereader[8])[3:-1]).split('\t') #30.3E, 29.8E strings
    longs = []                                       #30.3 , 29.8 float_values
    for lon in longitudes:
        if 'W' in lon:
            longs.append(-float(lon[:-1]))
        elif 'E' in lon:
            longs.append(float(lon[:-1]))
        else:
            longs.append(float(lon))
    matrix_data = pd.DataFrame(columns = longs)      #matrix DataFrame
    latitudes = []                                   #29.8N, 29.8S strings
    lats = []                                        # +29.8, -29.8 float_values
    for row in filereader[9:-1]:
        row = row[:-1]
        row = row.split('\t')
        if(row[0]) != '':
            latitudes.append(row[0])
            if 'S' in row[0]:
                lats.append(-float(row[0][:-1]))
                matrix_data.loc[-float(row[0][:-1])] = row[1:]
            elif 'N' in row[0]:
                lats.append(float(row[0][:-1]))
                matrix_data.loc[float(row[0][:-1])] = row[1:]
            else:
                lats.append(float(row[0]))
                matrix_data.loc[float(row[0])]
    return (matrix_data, scalar_badflag)

def ReadingTheVectorDataFile(filename):
    print('Reading the data file : ', filename)
    datafile = open(filename,'r+')
    filereader = datafile.readlines()
    datafile.close()
    vector_badflag = ''
    for val in ((filereader[4][:-1]).split(": "))[1]:
        if val != ' ':
            vector_badflag += val
    longitudes = ''
    for c in filereader[8][3:-3]:
        if c != ' ':
            longitudes += c
    longitudes = longitudes.split('\t')
    longs = []
    for lon in longitudes:
        if 'W' in lon:
            longs.append(-float(lon[:-1]))
        elif 'E' in lon:
            longs.append(float(lon[:-1]))
        else:
            longs.append(float(lon))
    matrix_data = pd.DataFrame(columns = longs)      #matrix DataFrame
    latitudes = []                                   #29.8N, 29.8S strings
    lats = []                                        # +29.8, -29.8 float_values
    for row in filereader[9:-1]:
        row = row[:-1]
        row = row.split('\t')
        if(row[0]) != '':
            latitudes.append(row[0])
            if 'S' in row[0]:
                lats.append(-float(row[0][:-1]))
                matrix_data.loc[-float(row[0][:-1])] = row[1:]
            elif 'N' in row[0]:
                lats.append(float(row[0][:-1]))
                matrix_data.loc[float(row[0][:-1])] = row[1:]
            else:
                lats.append(float(row[0]))
                matrix_data.loc[float(row[0])] = row[1:]
    return (matrix_data, vector_badflag)
