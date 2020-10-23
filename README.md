# Data Visualization

- Multi-Purpose Data Visualizer.

- Data sets are taken from INCOIS website. Link to the website : incois.gov.in/portal/index.jsp

- Part of Data Visualization Course Project.

- Data used August 2016 Ocean Data :
    - Scalar Data - `Potential Temperature, Salinity, Tropical Heat Potential, Zonal Current Speed, Meridional Current Speed`
    - Vector Data - `Zonal and Meridional Current Directions`

- Command to run the data visualization server - ```python3 visualization.py```

- Access the main page of the project on the following route - `http://0.0.0.0:5000/IMT2015042_Project or http://localhost:5000/IMT2015042_Project`

- Packages Required for running the Project :
    - flask
    - numpy
    - matplotlib
    - pandas
    - scipy

- Data and Algorithms Used : 
    - Data Dimension : 2D & 3D
    - Data Type : Scalar and Vector Data
    - Interpolation Type : Bilinear and Bicubic Interpolation
    - Visualizations : Contour Maps, Elevation Plots and Hedgehog Plots

- Sample Images :
    - Scalar Visualization, Potential Temperature - Bilinear Interpolation - 2D plot - Oranges_r colormap
      ![Plot](https://github.com/SuryaSri/Data_Visualization_Assignment-1/blob/master/static/Aug-2016-potential-temperature-180x188.txt_Bilinear_Interpolation_2D_Oranges_r.png?raw=True)
    - Scalar Visualization, Potential Temperature - Bilinear Interpolation - 3D plot - viridis colormap
      ![Plot]()
    - Vector Visualization, Zonal Current and Meridional Hedgehog Plot - BuPu_r colormap
      ![Plot](https://github.com/SuryaSri/Data_Visualization_Assignment-1/blob/master/static/Aug-2016-zonal-current-181x189.txt_Aug-2016-meridional-current-181x189.txt_Hedgehog_BuPu_r.png?raw=True)
