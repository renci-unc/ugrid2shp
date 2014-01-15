netCDF4-python-ADCIRC-shapefile
===============================

Using a netCDF4 file output from ADCIRC or Adcirc-lite, this tool allows a user to visualize a grid with a contoured layer in matplotlib, and output that view to an ESRI Shapefile using Shapely and Fiona.


###System Requirements
- Python 2.7.x
- Shapely (https://pypi.python.org/pypi/Shapely/1.3.0)
- Fiona (Geospatial Data Abstraction Library (GDAL) OGR interface; https://pypi.python.org/pypi/Fiona)
- netCDF4 C library (with opendap enabled, if opendap/remote functionality is desired)
- libhdf5 C library (dependency of netCDF4; http://www.unidata.ucar.edu/downloads/netcdf/index.jsp)
- libcurl (dependency of opendap; http://curl.haxx.se/libcurl/)
- netcdf4-python (netCDF4/libhdf5 C libraries must be installed first; https://pypi.python.org/pypi/netCDF4)

###Notes: 
On a mac using the homebrew package manager (http://brew.sh/), the homebrew/science tap (https://github.com/Homebrew/homebrew-science) can be used to simplify installation of the requisite HDF5 and netCDF4
C libraries needed for building netcdf4-python, but be sure to confirm OPeNDAP compatibility if taking this approach.

