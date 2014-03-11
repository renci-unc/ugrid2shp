 netCDF4-ugrid-shapefile-gen
===============================

This tool allows a user to visualize a CF-UGRID compliant netCDF file with a contoured layer in matplotlib, and output that view to an ESRI Shapefile using Shapely and Fiona.


###System Requirements
- Python 2.7.x
- Shapely 
    - https://pypi.python.org/pypi/Shapely/1.3.0
- Fiona (Geospatial Data Abstraction Library (GDAL) OGR interface
    - https://pypi.python.org/pypi/Fiona
- netCDF4 C library 
    - Be sure to install this with OPeNDAP enabled in the configuration.
- libhdf5 C library 
    - Dependency for NetCDF4.
    - http://www.unidata.ucar.edu/downloads/netcdf/index.jsp
- libcurl 
    - OPeNDAP dependency. 
    - http://curl.haxx.se/libcurl/
- netcdf4-python 
    - The netCDF4/libhdf5 C libraries must be installed before installing netcdf4-python.
    - https://pypi.python.org/pypi/netCDF4
- shell-doctest 
    - This python library is needed to run doc tests.
    - https://code.google.com/p/shell-doctest/
    - Install with `pip install https://pypi.python.org/packages/source/s/shelldoctest/shelldoctest-0.2.tar.gz#md5=94090432329f8db0fc5a3227bd2dfde9`

###Notes: 
On a mac using the homebrew package manager (http://brew.sh/), the homebrew/science tap (https://github.com/Homebrew/homebrew-science) can be used to simplify installation of the HDF5 and netCDF4 C libraries needed for building netcdf4-python, but be sure to confirm OPeNDAP compatibility if taking this approach. **[how does one confirm this?]**

###Helpful hints:
Run `$ python adcirc_netcdf_viz.py -h` for help

###Example usage:

**[point this example at a maxele file on RENCI's THREDDs server...]**

    $ python adcirc_netcdf_viz.py -n twm_example -o test -v maxele_prediction -a 0 -b 11


###Example output:

    Getting data from url=twm_example.nc...
    [u'x', u'y', u'maxele', u'maxele_prediction', u'element', u'bnd']
    Shape of lon is (608114)
    Shape of lat is (608114)
    Shape of nv is (1200767, 3)
    Max of lon is (-60)
    Max of lat is (45)
    Max of nv is (608113)
    elapsed time= 1 seconds
    var[0]: -99999.0
    Triangulating ...
    elapsed time= 0 seconds
    Making contours in figure ...
    Calling tricontourf  ...
    elapsed time= 2 seconds
    Saving figure as test.png
    Extracting contour shapes from tricontourf object ...
    Writing shapes to test.shp
    elapsed time= 16 seconds
    Writing prj to test.prj



