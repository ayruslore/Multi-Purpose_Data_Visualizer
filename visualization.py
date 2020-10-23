from flask import Flask, render_template, request, url_for
import numpy as np
import os
from shutil import copyfile

from reader_helper import *
from dataprocessing_helper import *
from visualization_helper import *

global scalar_files, vector_files
global scalar_dataframes, vector_dataframes, scalar_bilinear_interpolated_data, scalar_bicubic_interpolated_data
global contour_data, contour_values_plot
global badflags, colormaps

scalar_files = ['Aug-2016-potential-temperature-180x188.txt', 'Aug-2016-salinity-180x188.txt', 'Aug-2016-tropical-heat-potential-180x188.txt', 'Aug-2016-zonal-current-181x189.txt', 'Aug-2016-meridional-current-181x189.txt']
vector_files = [['Aug-2016-zonal-current-181x189.txt', 'Aug-2016-meridional-current-181x189.txt']]

scalar_dataframes = {}
scalar_bilinear_interpolated_data  = {}
scalar_bicubic_interpolated_data = {}
vector_dataframes = {}

contour_data = {}
contour_values_plot = {}

badflags = {}

colormaps = ['viridis', 'viridis_r', 'plasma', 'plasma_r', 'inferno', 'inferno_r', 'magma', 'magma_r', 'Greys', 'Greys_r', 'Purples', 'Purples_r', 'Blues', 'Blues_r', 'Greens', 'Greens_r', 'Oranges', 'Oranges_r', 'Reds', 'Reds_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'OrRd', 'OrRd_r', 'PuRd', 'PuRd_r', 'RdPu', 'RdPu_r', 'BuPu', 'BuPu_r', 'GnBu', 'GnBu_r', 'PuBu', 'PuBu_r', 'YlGnBu', 'YlGnBu_r', 'PuBuGn', 'PuBuGn_r', 'BuGn', 'BuGn_r', 'YlGn', 'YlGn_r', 'binary', 'binary_r', 'gist_yarg', 'gist_yarg_r', 'gist_gray', 'gist_gray_r', 'gray', 'gray_r', 'bone', 'bone_r', 'pink', 'pink_r', 'spring', 'spring_r', 'summer', 'summer_r', 'autumn', 'autumn_r', 'winter', 'winter_r', 'cool', 'cool_r', 'Wistia', 'Wistia_r', 'hot', 'hot_r', 'afmhot', 'afmhot_r', 'gist_heat', 'gist_heat_r', 'copper', 'copper_r', 'PiYG', 'PiYG_r', 'PRGn', 'PRGn_r', 'BrBG', 'BrBG_r', 'PuOr', 'PuOr_r', 'RdGy', 'RdGy_r', 'RdBu', 'RdBu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Spectral', 'Spectral_r', 'coolwarm', 'coolwarm_r', 'bwr', 'bwr_r', 'seismic', 'seismic_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'Paired', 'Paired_r', 'Accent', 'Accent_r', 'Dark2', 'Dark2_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'flag', 'flag_r', 'prism', 'prism_r', 'ocean', 'ocean_r', 'gist_earth', 'gist_earth_r', 'terrain', 'terrain_r', 'gist_stern', 'gist_stern_r', 'gnuplot', 'gnuplot_r', 'gnuplot2', 'gnuplot2_r', 'CMRmap', 'CMRmap_r', 'cubehelix', 'cubehelix_r', 'brg', 'brg_r', 'hsv', 'hsv_r', 'gist_rainbow', 'gist_rainbow_r', 'rainbow', 'rainbow_r', 'jet', 'jet_r', 'nipy_spectral', 'nipy_spectral_r', 'gist_ncar', 'gist_ncar_r']


def mainfunction():
    print('Reading the Data Files!!')
    global scalar_files, vector_files, badflags
    global scalar_dataframes, vector_dataframes, scalar_bilinear_interpolated_data, scalar_bicubic_interpolated_data, contour_data
    scalar_dataframes = {}
    for i in range( len(scalar_files) ):
        if i == 4 or i == 3:
            df, badval = ReadingTheVectorDataFile( scalar_files[i] )
        else:
            df, badval = ReadingTheScalarDataFile( scalar_files[i] )
        scalar_dataframes[ scalar_files[i] ] = df
        badflags[ scalar_files[i] ] = badval
    scalar_bilinear_interpolated_data  = {}
    for i in range( len(scalar_files) ):
        new_df = PerformBilinearInterpolation( scalar_dataframes[ scalar_files[i] ], 5, badflags[ scalar_files[i] ] )
        scalar_bilinear_interpolated_data[ scalar_files[i] ] = new_df
    scalar_bicubic_interpolated_data = {}
    for i in range( len(scalar_files) ):
        new_df = PerformBicubicInterpolation( scalar_dataframes[ scalar_files[i] ], 5, badflags[ scalar_files[i] ] )
        scalar_bicubic_interpolated_data[ scalar_files[i] ] = new_df
    contour_data = {}
    contour_values_plot = {}
    for i in range( len(scalar_files) ):
        contourvalues = np.linspace( min( scalar_bilinear_interpolated_data[ scalar_files[i] ]['value'] ), max( scalar_bilinear_interpolated_data[ scalar_files[i] ]['value'] ), 15, endpoint = False )
        contours = MarchingSquares( scalar_dataframes[ scalar_files[i] ], contourvalues[1:], badflags[ scalar_files[i] ] )
        contour_data[ scalar_files[i] ] = contours
        contour_values_plot[ scalar_files[i] ] = contourvalues
    vector_dataframes = {}
    for i in range( len(vector_files) ):
        u_df, u_bad = ReadingTheVectorDataFile( vector_files[i][0] )
        v_df, v_bad = ReadingTheVectorDataFile( vector_files[i][1] )
        vector_dataframes[ vector_files[i][0] ] = u_df
        vector_dataframes[ vector_files[i][1] ] = v_df
        badflags[ vector_files[i][0] ] = u_bad
        badflags[ vector_files[i][1] ] = v_bad
    print('Data is Ready!!')

app = Flask(__name__)

@app.route('/IMT2015042_Project')
def AssignmentMainPage():
    global scalar_files, vector_files, colormaps
    data = { 's': scalar_files, 'v': vector_files }
    scalar_data_options = { 'interp' : ['Bilinear_Interpolation', 'Bicubic_Interpolation'], 'dim' : ['2D', '3D'], 'cmaps' : colormaps }
    vector_data_options = { 'plots' : ['Hedgehog'], 'cmaps' : colormaps }
    return render_template('index.html', files = data, scalaroptions = scalar_data_options, vectoroptions = vector_data_options )

@app.route('/scalar_visualize/<sv_filename>/<sv_interpolation>/<sv_dim>/<sv_cmap>')
def scalar_visualize( sv_filename, sv_interpolation, sv_dim, sv_cmap ):
    global scalar_dataframes, vector_dataframes, scalar_bilinear_interpolated_data, scalar_bicubic_interpolated_data, badflags
    global scalar_files, vector_files
    data = { 's': scalar_files, 'v': vector_files }
    scalar_data_options = { 'interp' : ['Bilinear_Interpolation', 'Bicubic_Interpolation'], 'dim' : ['2D', '3D'], 'cmaps' : colormaps }
    vector_data_options = { 'plots' : ['Hedgehog'], 'cmaps' : colormaps }
    data_options = { 'val' : 0, 'sf_file' : sv_filename, 'sf_interp' : sv_interpolation, 'sf_dim' : sv_dim, 'sf_cmap' : sv_cmap }
    name = 'static/' + sv_filename + '_' + sv_interpolation + '_' + sv_dim + '_' + sv_cmap + '.png'
    if os.path.exists(name) :
        return render_template('index2.html', files = data, scalaroptions = scalar_data_options, vectoroptions = vector_data_options, optiondata = data_options, imagename = name[7:] )
    else:
        if sv_dim == '2D' :
            if sv_interpolation == 'Bilinear_Interpolation':
                plotname = Make2Dplot( scalar_bilinear_interpolated_data[sv_filename], contour_data[sv_filename], sv_cmap, data_options )
            else :
                plotname = Make2Dplot( scalar_bicubic_interpolated_data[sv_filename], contour_data[sv_filename], sv_cmap, data_options )
        else:
            if sv_interpolation == 'Bilinear_Interpolation':
                plotname = Make3DElevationMap( scalar_bilinear_interpolated_data[sv_filename], sv_cmap, data_options )
            else :
                plotname = Make3DElevationMap( scalar_bicubic_interpolated_data[sv_filename], sv_cmap, data_options )
        return render_template('index2.html', files = data, scalaroptions = scalar_data_options, vectoroptions = vector_data_options, optiondata = data_options, imagename = plotname )

@app.route('/vector_visualize/<u_filename>/<vv_plot>/<vv_cmap>')
def vector_visualize( u_filename, vv_plot, vv_cmap ):
    global scalar_files, vector_files, vector_dataframes, badflags
    data = { 's': scalar_files, 'v': vector_files }
    scalar_data_options = { 'interp' : ['Bilinear_Interpolation', 'Bicubic_Interpolation'], 'dim' : ['2D', '3D'], 'cmaps' : colormaps }
    vector_data_options = { 'plots' : ['Hedgehog'], 'cmaps' : colormaps }
    data_options = { 'val' : 1, 'u_file' : u_filename, 'vv_plot' : vv_plot, 'vv_cmap' : vv_cmap }
    for i in range( len(vector_files) ):
        if vector_files[i][0] == u_filename:
            v_filename = vector_files[i][1]
    data_options[ 'v_file' ] = v_filename
    name = 'static/' + u_filename + '_' + v_filename + '_' + vv_plot + '_' + vv_cmap + '.png'
    if os.path.exists(name) :
        return render_template('index3.html', files = data, scalaroptions = scalar_data_options, vectoroptions = vector_data_options, optiondata = data_options, imagename = name[7:] )
    else:
        if vv_plot == 'Hedgehog' :
            plotname = MakeHedgehogplot( vector_dataframes[u_filename], vector_dataframes[v_filename], data_options, { 'u' : badflags[u_filename], 'v' : badflags[v_filename] }, vv_cmap )
        return render_template('index3.html', files = data, scalaroptions = scalar_data_options, vectoroptions = vector_data_options, optiondata = data_options, imagename = plotname )

if __name__ == '__main__':
    mainfunction()
    print(badflags)
    app.run( host = '0.0.0.0', port = 5000, debug = True)
