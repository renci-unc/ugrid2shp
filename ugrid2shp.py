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


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--debug',
                        dest='debug',
                        action='store_true',
                        help='display diagnostics')
    parser.add_argument('-s', '--silent',
                        dest='silent',
                        action='store_true',
                        help='no screen diagnostic output')
    parser.add_argument('-w', '--write_image',
                        dest='write_image',
                        action='store_true',
                        help='write matplotlib image to a file <outfile>.png')
    parser.add_argument('-x', '--show_image',
                        dest='show_image',
                        action='store_true',
                        help='display matplotlib image, ' \
                             'user must close before continuing')
    parser.add_argument('-z', '--no_zip',
                        dest='no_zip',
                        action='store_true',
                        help='no zip file output')
    parser.add_argument('-n', '--ncfilename',
                        default='maxele.63.nc',
                        help='netCDF file to read from, ' \
                             'or a URL to an OPeNDAP file')
    parser.add_argument('ncfilename',
                        default='maxele.63.nc',
                        action='store_true')
    return parser.parse_args('-h'.split())


def main():

    # Default parameter values.
    ncfilename = 'maxele.63.nc'
    outfilename = 'outShape'
    NcVarName = 'zeta_max'
    MinVal = 0
    MaxVal = 10
    AxisLims = []
    NumLevels = 11
    silent = False
    write_image = False
    show_image = False
    no_zip = False
    debug = False
    ProjStr = 'GEOGCS["GCS_WGS_1984",' \
              'DATUM["D_WGS_1984",' \
              'SPHEROID["WGS_1984",6378137.0,298.257223563]],' \
              'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'

    imagefilename = outfilename + '.png'
    shapefilename = outfilename + '.shp'
    prjfilename = outfilename + '.prj'
    zipfilename = outfilename + '.zip'
    readmefilename = 'README.txt'

    # get timestamp
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if debug:
        print "Create time " + st

    if not ncfilename:
        no_ncfilename_msg = \
            "You must pass a netCDF filename or url as an argument. " \
            "Use the -n or --NcFileName argument to do this."
        raise Exception(no_ncfilename_msg)

    url = ncfilename
    path, ncfile = os.path.split(url)
    if not path:
        path = 'file://'
    if not silent:
        print path + ncfile

    # end of url must have .nc
    # if url[-3:] != '.nc': url=url+'.nc'

    # get stuff from netCDF file
    if not silent:
        print 'Getting data from %s... ' % url

    nc = netCDF4.Dataset(url)
    vars = nc.variables
    if debug:
        print vars.keys()

    # get some global attributes
    model = getattr(nc, 'model')
    grid = getattr(nc, 'agrid')
    inst = getattr(nc, 'institution')

    lon = vars['x'][:]
    lat = vars['y'][:]
    var = vars[NcVarName]
    units = var.units
    data = vars[NcVarName][:]
    if len(data.shape) > 1:
        data = data[0, :]
    elems = vars['element'][:, :] - 1  # Move to 0-indexing by subtracting 1
    plot_title = 'MatPlotLib plot of ' + NcVarName + ' in ' + ncfile

    if debug:
        print "\n   Shape of lon is (%i)" % lon.shape
        print "   Shape of lat is (%i)" % lat.shape
        print "   Shape of nv is (%i, %i)" % elems.shape
        print "   Max of lon is (%i)" % lon.max()
        print "   Max of lat is (%i)" % lat.max()
        print "   Max of nv is (%i)" % elems.max()
        print "   First value in var: " + str(data[0]) + '\n'

    if not silent:
        print 'Triangulating ...'
    tri = Tri.Triangulation(lon, lat, triangles=elems)

    if not silent:
        print 'Making contours in figure ...'
    fig = plt.figure(figsize=(10, 10))
    plt.subplot(111, aspect=(1.0 / cos(mean(lat) * pi / 180.0)))
    levels = linspace(MinVal, MaxVal, num=NumLevels)

    if not silent:
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
    if not AxisLims:
        AxisLimsSplit = AxisLims.split(',')
        AxisLims = map(float, AxisLimsSplit)
        axis(AxisLims)

    if write_image:
        if not silent:
            print "Saving figure as " + imagefilename
        savefig(imagefilename)

    if show_image:
        print "\nDisplay window must be closed " \
              "before shapefile can be written. \n"
        show()

    # this is the meat, as per Rusty Holleman
    if not silent:
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
    if not silent:
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

    if not silent:
        print "Writing prj to " + prjfilename

    prj_file = open(prjfilename, 'w')
    prj_file.write(ProjStr)
    prj_file.close()

    # write a README file
    rmf = open(readmefilename, mode='w')
    rmf.write('CreateTime: {0}\n'.format(st))
    rmf.write('Model: {0}\n'.format(model))
    rmf.write('Grid: {0}\n'.format(grid))
    rmf.write('Institution: {0}\n'.format(inst))
    rmf.write('Url: {0}\n'.format(path))
    rmf.write('File: {0}\n'.format(ncfile))
    rmf.write('ProjStr: {0}\n'.format(ProjStr))
    rmf.write('Units: {0}\n'.format(units))
    rmf.close()

    if not no_zip:
        if not silent:
            print 'Flushing zip file to ' + zipfilename
        zf = zipfile.ZipFile(zipfilename, mode='w')
        zf.write(outfilename + '.shp')
        if os.path.isfile(outfilename + '.prj'):
            zf.write(outfilename + '.prj')
        if os.path.isfile(outfilename + '.cpg'):
            zf.write(outfilename + '.cpg')
        if os.path.isfile(outfilename + '.shx'):
            zf.write(outfilename + '.shx')
        if os.path.isfile(outfilename + '.dbf'):
            zf.write(outfilename + '.dbf')
        zf.write(readmefilename)
        zf.close()

        # Remove working files
        if os.path.isfile(outfilename + '.prj'):
            os.remove(outfilename + '.prj')
        if os.path.isfile(outfilename + '.cpg'):
            os.remove(outfilename + '.cpg')
        if os.path.isfile(outfilename + '.shx'):
            os.remove(outfilename + '.shx')
        if os.path.isfile(outfilename + '.dbf'):
            os.remove(outfilename + '.dbf')
        os.remove(outfilename + '.shp')

    # try reading the Shapefile back in
    # c = fiona.open(shapefilename, 'r')

if __name__ == "__main__":
    main()
