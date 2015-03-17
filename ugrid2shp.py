#
# ugrid2shp.py -  shapefile generator for CF-UGRID compliant netCDF files
#
# Idea from Rusty Holleman and Rich Signell (shapely/fiona)
# Code by Brian Blanton, RENCI
#

from pylab import *
import matplotlib.tri as Tri
import matplotlib.pyplot as plt
from shapely.geometry import mapping, Polygon
import fiona
import netCDF4
import datetime
import time
import sys
import argparse
import zipfile
import os

defaults = {'ProjStr': 'GEOGCS["GCS_WGS_1984",'
                       'DATUM["D_WGS_1984",'
                       'SPHEROID["WGS_1984",6378137.0,298.257223563]],'
                       'PRIMEM["Greenwich",0.0],'
                       'UNIT["Degree",0.0174532925199433]]',
            'axis_limits': [],
            'debug': False,
            'maxval': 10,
            'minval': 0,
            'nc_var_name': 'zeta_max',
            'ncfilename': 'maxele.63.nc',
            'no_zip': False,
            'numlevels': 11,
            'outfilename': 'outShape',
            'show_image': False,
            'silent': False,
            'write_image': False}

def parse_args(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--debug',
                        dest='debug',
                        action='store_true',
                        help='Display diagnostics.')
    parser.add_argument('-s', '--silent',
                        dest='silent',
                        action='store_true',
                        help='No screen diagnostic output.')
    parser.add_argument('-w', '--writeimage',
                        dest='write_image',
                        action='store_true',
                        help='Write matplotlib image to a file <outfile>.png.')
    parser.add_argument('-x', '--showimage',
                        dest='show_image',
                        action='store_true',
                        help='Display matplotlib image, '
                             'user must close before continuing.')
    parser.add_argument('-z', '--nozip',
                        dest='no_zip',
                        action='store_true',
                        help='No zip file output.')
    parser.add_argument('-n', '--ncfilename',
                        dest='ncfilename',
                        action='store',
                        metavar='NC_FILE_NAME',
                        default=defaults['ncfilename'],
                        help='Path to NetCDF file to read, '
                             'or a URL to an OPeNDAP resource.')
    parser.add_argument('-o', '--outfilename',
                        dest='outfilename',
                        action='store',
                        metavar='OUTPUT_FILE_NAME',
                        default=defaults['outfilename'],
                        help='Filename to write as shapefile.')
    parser.add_argument('-v', '--ncvarname',
                        dest='nc_var_name',
                        action='store',
                        metavar='NC_VAR_NAME',
                        default=defaults['nc_var_name'],
                        help='NetCDF variable name to render.')
    parser.add_argument('-a', '--minval',
                        type=int,
                        dest='minval',
                        action='store',
                        metavar="MIN_VAL",
                        default=defaults['minval'],
                        help='Smallest scalar value to render.')
    parser.add_argument('-b', '--maxval',
                        type=int,
                        dest='maxval',
                        action='store',
                        metavar='MAX_VAL',
                        default=defaults['maxval'],
                        help='Largest scalar value to render.')
    parser.add_argument('-c', '--numlevels',
                        type=int,
                        dest='numlevels',
                        action='store',
                        metavar='NUM_LEVELS',
                        default=defaults['numlevels'],
                        help='Number of contour levels.')
    parser.add_argument('-l', '--axislimits',
                        nargs=4,
                        dest='axis_limits',
                        action='store',
                        metavar=('X0', 'Y0', 'X1', "Y1"),
                        default=defaults['axis_limits'],
                        help='Bounding box list of coordinates.')
    parser.add_argument('-p', '--proj',
                        dest="ProjStr",
                        action='store',
                        metavar="PROJECTION_STRING",
                        default=defaults['ProjStr'],
                        help="Projection string as Well Known Text (WKT).")

    return parser.parse_args(argv)


def main(argv):

    args = parse_args(argv)

    imagefilename = args.outfilename + '.png'
    shapefilename = args.outfilename + '.shp'
    prjfilename = args.outfilename + '.prj'
    zipfilename = args.outfilename + '.zip'
    readmefilename = 'README.txt'

    # get timestamp
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if args.debug:
        print "Create time " + st

    url = args.ncfilename
    path, ncfile = os.path.split(url)
    if not path:
        path = 'file://'
    if not args.silent:
        print path + ncfile

    # end of url must have .nc
    # if url[-3:] != '.nc': url=url+'.nc'

    # get stuff from netCDF file
    if not args.silent:
        print 'Getting data from %s... ' % url

    nc = netCDF4.Dataset(url)
    ncvars = nc.variables
    if args.debug:
        print ncvars.keys()

    # get some global attributes
    model = getattr(nc, 'model')
    grid = getattr(nc, 'agrid')
    inst = getattr(nc, 'institution')

    lon = ncvars['x'][:]
    lat = ncvars['y'][:]
    var = ncvars[args.nc_var_name]
    units = var.units
    data = ncvars[args.nc_var_name][:]
    if len(data.shape) > 1:
        data = data[0, :]
    elems = ncvars['element'][:, :] - 1  # Move to 0-indexing by subtracting 1
    plot_title = 'MatPlotLib plot of ' + args.nc_var_name + ' in ' + ncfile

    if args.debug:
        print "\n   Shape of lon is (%i)" % lon.shape
        print "   Shape of lat is (%i)" % lat.shape
        print "   Shape of nv is (%i, %i)" % elems.shape
        print "   Max of lon is (%i)" % lon.max()
        print "   Max of lat is (%i)" % lat.max()
        print "   Max of nv is (%i)" % elems.max()
        print "   First value in var: " + str(data[0]) + '\n'

    if not args.silent:
        print 'Triangulating ...'
    tri = Tri.Triangulation(lon, lat, triangles=elems)

    if not args.silent:
        print 'Making contours in figure ...'
    fig = plt.figure(figsize=(10, 10))
    plt.subplot(111, aspect=(1.0 / cos(mean(lat) * pi / 180.0)))
    levels = linspace(args.minval, args.maxval, num=args.numlevels)

    if not args.silent:
        print 'Calling tricontourf  ...'
    contour = tricontourf(tri, data, levels=levels, shading='faceted')
    cbar = fig.colorbar(contour, orientation='vertical', ticks=levels)
    cbar.set_label(units)
    title(plot_title)
    figtext(.5,
            .05,
            'URL: ' + path + ncfile,
            size='small',
            horizontalalignment='center')

    # This takes the axis limit string arg and converts it to a list.
    # Then it converts that list to floats.
    if args.axis_limits:
        axis_limits = map(float, args.axis_limits)
        axis(axis_limits)

    if args.write_image:
        if not args.silent:
            print "Saving figure as " + imagefilename
        savefig(imagefilename)

    if args.show_image:
        print "\nDisplay window must be closed " \
              "before shapefile can be written. \n"
        show()

    # this is the meat, as per Rusty Holleman
    if not args.silent:
        print 'Extracting contour shapes from tricontourf object ...'
    geoms = []
    # create list of tuples (geom, vmin, vmax)
    for colli, coll in enumerate(contour.collections):
        vmin, vmax = contour.levels[colli:colli + 2]
        for p in coll.get_paths():
            p.simplify_threshold = 0.0
            polys = p.to_polygons()
            # Don't append an empty polygon to the geometry
            # or it will screw up the indexing.
            if polys:
                # Don't append holes without at least three coordinates
                polys[1:] = [poly for poly in polys[1:] if poly.shape[0] > 2]
                geoms.append((Polygon(polys[0], polys[1:]), vmin, vmax))

    # this is the other meat, as per Rusty Holleman
    if not args.silent:
        print "Writing shapes to " + shapefilename
    schema = {'geometry': 'Polygon',
              'properties': {'vmin': 'float',
                             'vmax': 'float'}}
    with fiona.open(shapefilename, 'w', 'ESRI Shapefile', schema) as c:
        for geom in geoms:
            c.write({
                'geometry': mapping(geom[0]),
                'properties': {'vmin': geom[1], 'vmax': geom[2]},
            })

    if not args.silent:
        print "Writing prj to " + prjfilename

    prj_file = open(prjfilename, 'w')
    prj_file.write(args.ProjStr)
    prj_file.close()

    # write a README file
    rmf = open(readmefilename, mode='w')
    rmf.write('CreateTime: {0}\n'.format(st))
    rmf.write('Model: {0}\n'.format(model))
    rmf.write('Grid: {0}\n'.format(grid))
    rmf.write('Institution: {0}\n'.format(inst))
    rmf.write('Url: {0}\n'.format(path))
    rmf.write('File: {0}\n'.format(ncfile))
    rmf.write('ProjStr: {0}\n'.format(args.ProjStr))
    rmf.write('Units: {0}\n'.format(units))
    rmf.close()

    if not args.no_zip:
        if not args.silent:
            print 'Flushing zip file to ' + zipfilename
        zf = zipfile.ZipFile(zipfilename, mode='w')
        zf.write(args.outfilename + '.shp')
        if os.path.isfile(args.outfilename + '.prj'):
            zf.write(args.outfilename + '.prj')
        if os.path.isfile(args.outfilename + '.cpg'):
            zf.write(args.outfilename + '.cpg')
        if os.path.isfile(args.outfilename + '.shx'):
            zf.write(args.outfilename + '.shx')
        if os.path.isfile(args.outfilename + '.dbf'):
            zf.write(args.outfilename + '.dbf')
        zf.write(readmefilename)
        zf.close()

        # Remove working files
        if os.path.isfile(args.outfilename + '.prj'):
            os.remove(args.outfilename + '.prj')
        if os.path.isfile(args.outfilename + '.cpg'):
            os.remove(args.outfilename + '.cpg')
        if os.path.isfile(args.outfilename + '.shx'):
            os.remove(args.outfilename + '.shx')
        if os.path.isfile(args.outfilename + '.dbf'):
            os.remove(args.outfilename + '.dbf')
        os.remove(args.outfilename + '.shp')

    # try reading the Shapefile back in
    # c = fiona.open(shapefilename, 'r')

if __name__ == "__main__":
    main(sys.argv[1:])
