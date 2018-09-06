import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import *
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np
import time

def Make2Dplot( data, contours, colormap, dataname ):
    print('Plotting 2D scatter plot and contours.')
    fig = plt.figure()
    ax = plt.subplot(111)
    for contour in contours :
        for lines in contour :
            x = []
            y = []
            for point in lines :
                x.append( point[0] )
                y.append( point[1] )
            ax.plot(x, y, '-', color = "black", linewidth = 1)
    cmap = cm.get_cmap(colormap)
    norm = mpl.colors.Normalize( vmin = min( data['value'] ), vmax = max( data['value'] ) )
    map_function = cm.ScalarMappable(norm = norm, cmap = cmap)
    color_data = map_function.to_rgba( data['value'] )
    ax.scatter(data['long'], data['lat'], c = color_data, s = 1, alpha = 0.6 )
    name = 'static/' + dataname['sf_file'] + '_' + dataname['sf_interp'] + '_' + dataname['sf_dim'] + '_' + dataname['sf_cmap'] + '.png'
    fig.savefig(name)
    plt.close(fig)
    time.sleep(1)
    return name[7:]

def Make3DElevationMap( data, colormap, dataname ):
    print('Plotting 3D Elevation Mapping and the contours.')
    cmap = cm.get_cmap(colormap)
    norm = mpl.colors.Normalize( vmin = min( data['value'] ), vmax = max( data['value'] ) )
    map_function = cm.ScalarMappable(norm = norm, cmap = cmap)
    color_data = map_function.to_rgba( data['value'] )
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.view_init(azim = 40)
    ax.scatter3D( np.array(data['long']), np.array(data['lat']), np.array(data['value']), c = color_data )
    name = 'static/' + dataname['sf_file'] + '_' + dataname['sf_interp'] + '_' + dataname['sf_dim'] + '_' + dataname['sf_cmap'] + '.png'
    fig.savefig(name)
    plt.close(fig)
    time.sleep(1)
    return name[7:]

def MakeVectorData( U_file, V_file, badflag ):
    data = { 'long':[], 'lat':[], 'U':[], 'V':[], 'C':[] }
    longs = list(U_file.columns)
    lats = list(U_file.index)
    i = 0
    while i < len(lats):
        j = 0
        while j < len(longs):
            if badflag['u'] not in U_file.iat[i,j] and badflag['v'] not in V_file.iat[i,j]:
                data['long'].append(longs[j])
                data['lat'].append(lats[i])
                data['U'].append(float(U_file.iat[i,j]))
                data['V'].append(float(V_file.iat[i,j]))
                mag = ( (float(U_file.iat[i,j])**2) + (float(V_file.iat[i,j])**2) )**0.5
                data['C'].append(mag)
            j += 5
        i += 7
    return data

def MakeHedgehogplot(U_file, V_file, dataname, badflag, colormap ):
    print('Plotting Hedgehog plot!!')
    data = MakeVectorData(U_file, V_file, badflag)
    cmap = cm.get_cmap(colormap)
    norm = mpl.colors.Normalize( vmin = min( data['C'] ), vmax = max( data['C'] ) )
    map_function = cm.ScalarMappable(norm = norm, cmap = cmap)
    color_data = map_function.to_rgba( data['C'] )
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.quiver(data['long'], data['lat'], data['U'], data['V'], color = color_data )
    name = 'static/' + dataname['u_file'] + '_' + dataname['v_file'] + '_' + dataname['vv_plot'] + '_' + dataname['vv_cmap'] + '.png'
    fig.savefig(name)
    plt.close(fig)
    time.sleep(1)
    return name[7:]
