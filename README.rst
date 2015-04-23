Convert CF-UGRID netCDF files to GIS shapefiles
===============================================

This package computes a GIS shapefile from a CF-UGRID compliant netCDF file.
Contours are generated with matplotlib and then output using shapely and fiona.

To use as a package (using a list of default arguments):

    >>> from ugrid2shp import ugrid2shp, defaults
    >>> ugrid2shp(defaults)

To use as a script:

usage: ugrid2shp [-h] [-d] [-s] [-w] [-x] [-z] [-n NC_FILE_NAME]
                 [-o OUTPUT_FILE_NAME] [-v NC_VAR_NAME] [-a MIN_VAL]
                 [-b MAX_VAL] [-c NUM_LEVELS] [-l X0 Y0 X1 Y1]
                 [-p PROJECTION_STRING]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Display diagnostics. (default: False)
  -s, --silent          No screen diagnostic output. (default: False)
  -w, --writeimage      Write matplotlib image to a file <outfile>.png.
                        (default: False)
  -x, --showimage       Display matplotlib image, user must close before
                        continuing. (default: False)
  -z, --nozip           No zip file output. (default: False)
  -n NC_FILE_NAME, --ncfilename NC_FILE_NAME
                        Path to NetCDF file to read, or a URL to an OPeNDAP
                        resource. (default: maxele.63.nc)
  -o OUTPUT_FILE_NAME, --outfilename OUTPUT_FILE_NAME
                        Filename to write as shapefile. (default: outShape)
  -v NC_VAR_NAME, --ncvarname NC_VAR_NAME
                        NetCDF variable name to render. (default: zeta_max)
  -a MIN_VAL, --minval MIN_VAL
                        Smallest scalar value to render. (default: 0)
  -b MAX_VAL, --maxval MAX_VAL
                        Largest scalar value to render. (default: 10)
  -c NUM_LEVELS, --numlevels NUM_LEVELS
                        Number of contour levels. (default: 11)
  -l X0 Y0 X1 Y1, --axislimits X0 Y0 X1 Y1
                        Bounding box list of coordinates. (default: [])
  -p PROJECTION_STRING, --proj PROJECTION_STRING
                        Projection string as Well Known Text (WKT). (default:
                        GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS
                        _1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.
                        0],UNIT["Degree",0.0174532925199433]])

