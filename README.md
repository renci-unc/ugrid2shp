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
    - http://www.unidata.ucar.edu/downloads/netcdf/index.jsp
    - See notes section if installing on a mac - there is an easier way.
- libhdf5 C library 
    - Dependency for NetCDF4.
    - http://www.hdfgroup.org/HDF5/release/obtain5.html
    - See notes section if installing on a mac - there is an easier way.
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
On a mac using the homebrew package manager (http://brew.sh/), the homebrew/science tap (https://github.com/Homebrew/homebrew-science) can be used to simplify installation of the HDF5 and netCDF4 C libraries needed for building netcdf4-python. 
After installing homebrew, add the homebrew-science tap, then install the HDF5 and netCDF4 C libraries from the homebrew-science tap

###Helpful hints:
Run `$ python netcdf_viz.py -h` for help

###Example usage:

    $ python netcdf_viz.py -n  http://opendap.renci.org:1935/thredds/dodsC/ASGS/andrea/08/nc6b/blueridge.renci.org/fivemem/nhcConsensus/maxele.63.nc -o test_thredds -v zeta_max -a 0 -b 11 -s '-82, -72, 29, 39'


###Example output:
    Getting data from url=http://opendap.renci.org:1935/thredds/dodsC/ASGS/andrea/08/nc6b/blueridge.renci.org/fivemem/nhcConsensus/maxele.63.nc...    
    [u'time', u'x', u'y', u'element', u'adcirc_mesh', u'neta', u'nvdll', u'_nc4_non_coord_max_nvdll', u'ibtypee', u'nbdv', u'nvel', u'nvell', u'_nc4_non_coord_max_nvell',     u'ibtype', u'nbvv', u'depth', u'zeta_max']
    Shape of lon is (295328)
    Shape of lat is (295328)
    Shape of nv is (575512, 3)
    Max of lon is (-60)
    Max of lat is (45)
    Max of nv is (295327)
    var[0]: 0.749472089824
    Triangulating ...
    Making contours in figure ...
    Calling tricontourf  ...
    Saving figure as test_thredds.png
    Extracting contour shapes from tricontourf object ...
    Writing shapes to test_thredds.shp
    Writing prj to test_thredds.prj
### Open test_thredds.png to view a screenshot of the figure plotted with matplotlib:
![](https://raw.github.com/jessebikman/netCDF4-ugrid-shapefile-gen/master/test_thredds.png)
