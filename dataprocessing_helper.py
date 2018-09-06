import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def PerformBilinearInterpolation(matrix_data, num, badflag):
    print('Performing Bilinear interpolation on the data ', num, ' points')
    longs = list(matrix_data.columns)
    new_long_data = {}
    new_longs = list(matrix_data.columns)
    new_long_keys = []
    for index, row in matrix_data.iterrows():
        row = list(row)
        for j in range( len(row) - 1 ):
            newlongs = np.linspace( float(longs[j]), float(longs[j+1]), num, endpoint = False )
            if badflag in row[j] or badflag in row[j+1]:
                for z in range( len(newlongs[1:]) ):
                    if str(newlongs[1:][z]) not in new_long_data:
                        new_long_data[ str(newlongs[1:][z]) ] = [badflag]
                    else:
                        new_long_data[ str(newlongs[1:][z]) ].append( badflag )
            else:
                func = interp1d( [float(longs[j]), float(longs[j+1])], [float(row[j]), float(row[j+1])] )
                newvalues = func(newlongs[1:])
                for z in range( len(newlongs[1:]) ):
                    if str(newlongs[1:][z]) not in new_long_data:
                        new_long_data[ str(newlongs[1:][z]) ] = [ str(newvalues[z]) ]
                    else:
                        new_long_data[ str(newlongs[1:][z]) ].append( str(newvalues[z]) )
    for longi in new_long_data.keys():
        new_long_keys.append( float(longi) )
        new_longs.append( float(longi) )
    new_longs = sorted(new_longs)
    new_matrix_data = pd.DataFrame(columns = new_longs)
    i = 0
    lats = list(matrix_data.index)
    for lat in lats:
        row = []
        for longi in new_longs:
            if longi not in new_long_keys:
                row.append(matrix_data.loc[lat,longi])
            else:
                row.append(new_long_data[str(longi)][i])
        new_matrix_data.loc[lat] = row
        i += 1
    data = {'long' : [], 'lat' : [], 'value':[]}
    i = 0
    for index, row in new_matrix_data.iterrows():
        row = list(row)
        for j in range(len(row)):
            if badflag not in row[j]:
                data['lat'].append(lats[i])
                data['long'].append(new_longs[j])
                data['value'].append(float(row[j]))
        i += 1
    new_matrix_data = new_matrix_data.transpose()
    i = 0
    for index, row in new_matrix_data.iterrows():
        row = list(row)
        for j in range(len(row)-1):
            if badflag not in row[j] and badflag not in row[j+1]:
                new = np.linspace(lats[j], lats[j+1], num, endpoint = False)
                f = interp1d([lats[j], lats[j+1]], [float(row[j]), float(row[j+1])])
                new_val = f(new[1:])
                for z in range(len(new[1:])):
                    data['long'].append(new_longs[i])
                    data['lat'].append(new[1:][z])
                    data['value'].append(new_val[z])
        i += 1
    return data

def MarchingSquares(data, values, badflag):
    print('Finding contours from the data for ', len(values), ' points.')
    longs = list(data.columns)
    lats = list(data.index)
    allresult = []
    for val in values:
        result = []
        binary_data = []
        for index, row in data.iterrows():
            row = list(row)
            bindata = []
            for j in range(len(row)):
                if badflag not in row[j]:
                    if float(row[j]) >= float(val):
                        bindata.append(1)
                    else:
                        bindata.append(0)
                else:
                    bindata.append(0)
            binary_data.append(bindata)
        for i in range(len(lats)-1):
            for j in range(len(longs)-1):
                points = []
                if binary_data[i][j] + binary_data[i][j+1] == 1:
                    if badflag not in data.iat[i,j] and badflag not in data.iat[i,j+1]:
                        f = interp1d([float(data.iat[i,j]), float(data.iat[i,j+1])],[longs[j], longs[j+1]])
                        points.append((float(f(val)), lats[i]))
                if binary_data[i][j] + binary_data[i+1][j] == 1:
                    if badflag not in data.iat[i,j] and badflag not in data.iat[i+1,j]:
                        f = interp1d([float(data.iat[i,j]), float(data.iat[i+1,j])], [lats[i], lats[i+1]])
                        points.append((longs[j], float(f(val))))
                if binary_data[i+1][j] + binary_data[i+1][j+1] == 1:
                    if badflag not in data.iat[i+1,j] and badflag not in data.iat[i+1,j+1]:
                        f = interp1d([float(data.iat[i+1,j]), float(data.iat[i+1,j+1])], [longs[j], longs[j+1]])
                        points.append((float(f(val)), lats[i+1]))
                if binary_data[i][j+1] + binary_data[i+1][j+1] == 1:
                    if badflag not in data.iat[i,j+1] and badflag not in data.iat[i+1,j+1]:
                        f = interp1d([float(data.iat[i,j+1]), float(data.iat[i+1,j+1])], [lats[i], lats[i+1]])
                        points.append((longs[j+1], float(f(val))))
                result.append(points)
        allresult.append(result)
    final = []
    for result in allresult:
        lines = []
        for point in result:
            if len(point) != 0 and len(point) != 1:
                lines.append(point)
        final.append(lines)
    return final

def PerformBicubicInterpolation( matrix_data, num, badflag ):
    print('Performing Bicubic interpolation on the data ', num, ' points')
    longs = list(matrix_data.columns)
    new_long_data = {}
    new_longs = list(matrix_data.columns)
    new_long_keys = []
    for index, row in matrix_data.iterrows():
        row = list(row)
        for j in range( len(row) - 1 ):
            newlongs = np.linspace( float(longs[j]), float(longs[j+1]), num, endpoint = False )
            if badflag in row[j] or badflag in row[j+1]:
                for z in range( len(newlongs[1:]) ):
                    if str(newlongs[1:][z]) not in new_long_data:
                        new_long_data[ str(newlongs[1:][z]) ] = [badflag]
                    else:
                        new_long_data[ str(newlongs[1:][z]) ].append( badflag )
            else:
                func = interp1d( [float(longs[j]), float(longs[j+1])], [float(row[j]), float(row[j+1])], kind = 'linear' )
                newvalues = func(newlongs[1:])
                for z in range( len(newlongs[1:]) ):
                    if str(newlongs[1:][z]) not in new_long_data:
                        new_long_data[ str(newlongs[1:][z]) ] = [ str(newvalues[z]) ]
                    else:
                        new_long_data[ str(newlongs[1:][z]) ].append( str(newvalues[z]) )
    for longi in new_long_data.keys():
        new_long_keys.append( float(longi) )
        new_longs.append( float(longi) )
    new_longs = sorted(new_longs)
    new_matrix_data = pd.DataFrame(columns = new_longs)
    i = 0
    lats = list(matrix_data.index)
    for lat in lats:
        row = []
        for longi in new_longs:
            if longi not in new_long_keys:
                row.append(matrix_data.loc[lat,longi])
            else:
                row.append(new_long_data[str(longi)][i])
        new_matrix_data.loc[lat] = row
        i += 1
    data = {'long' : [], 'lat' : [], 'value':[]}
    i = 0
    for index, row in new_matrix_data.iterrows():
        row = list(row)
        for j in range(len(row)):
            if badflag not in row[j]:
                data['lat'].append(lats[i])
                data['long'].append(new_longs[j])
                data['value'].append(float(row[j]))
        i += 1
    new_matrix_data = new_matrix_data.transpose()
    i = 0
    for index, row in new_matrix_data.iterrows():
        row = list(row)
        for j in range(len(row)-1):
            if badflag not in row[j] and badflag not in row[j+1]:
                new = np.linspace(lats[j], lats[j+1], num, endpoint = False)
                f = interp1d( [lats[j], lats[j+1]], [float(row[j]), float(row[j+1])], kind = 'linear' )
                new_val = f(new[1:])
                for z in range(len(new[1:])):
                    data['long'].append(new_longs[i])
                    data['lat'].append(new[1:][z])
                    data['value'].append(new_val[z])
        i += 1
    return data
