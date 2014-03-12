from pylab import *
import matplotlib.tri as Tri
from shapely.geometry import mapping, Polygon
import fiona
import netCDF4
import datetime
import time
import sys
import getopt

def main(argv):
    
    # Defaults parameter values.
    ncfilename=None
    outfile='outShape'
    NcVariableName='zeta_max'
    MinVal = 0
    MaxVal = 11
    AxisLims = []
    NumberOfSamples = int(MaxVal - MinVal)

    try:
        opts, args = getopt.getopt(argv,"hn:o:v:a:b:c:s:",["ncfilename=","outfile=", "NcVariableName=", "MinVal=", "MaxVal=", "NumberOfSamples=", "AxisLims="])
    except getopt.GetoptError:
        print 'Option error: '
        print 'Run adcirc_netcdf_viz.py -h for help'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'adcirc_netcdf_viz.py -n <ncfilename> -o <outfile> -v <NcVariableName> -a <MinVal> -b <MaxVal> -c <NumberOfSamples> -s <AxisLims>'
            sys.exit()
        elif opt in ("-n", "--ncfilename"):
            ncfilename = arg
        elif opt in ("-o", "--outfile"):
            outfile = arg
        elif opt in ("-v", "--NcVariableName"):
            NcVariableName = arg
        elif opt in ("-a", "--MinVal"):
            MinVal = arg
        elif opt in ("-b", "--MaxVal"):
            MaxVal = arg
        elif opt in ("-c", "--NumberOfSamples"):
            NumberOfSamples = int(arg)
        elif opt in ("-s", "--AxisLims"):
            AxisLims = arg

    MinVal = float(MinVal)
    MaxVal = float(MaxVal)
    imagefilename=outfile+'.png'
    shapefilename=outfile+'.shp'
    prjfilename=outfile+'.prj'

    if ncfilename == None:
        raise Exception("You must pass a netCDF4 filename as an argument. Use the -n or --ncfilename argument to do this.")
    url = ncfilename
    titl='ADCIRC';
    if url[-3:] != '.nc':
        url=url+'.nc'
    vname=NcVariableName
    start=datetime.datetime(2008, 9, 13, 6, 0, 0)

    print 'Getting data from url=%s... ' % url

    nc=netCDF4.Dataset(url).variables
    nc.keys()
    print nc.keys()
    lon = nc['x'][:]
    lat = nc['y'][:]
    # Move to 0-indexing by subtracting 1
    nv = nc['element'][:,:]-1

    print "Shape of lon is (%i)" % lon.shape
    print "Shape of lat is (%i)" % lat.shape
    print "Shape of nv is (%i, %i)" % nv.shape

    print "Max of lon is (%i)" % lon.max()
    print "Max of lat is (%i)" % lat.max()
    print "Max of nv is (%i)" % nv.max()

    # time_var = nc['time']
    # dtime = netCDF4.num2date(time_var[:],time_var.units)
    #istart = netCDF4.date2index(start,time_var,select='nearest')
    #istart=1
    #var = nc[vname][istart,:]    
    var = nc[vname][:]
    print "var[0]: " + str(var[0])

    print 'Triangulating ...'
    tri = Tri.Triangulation(lon,lat, triangles=nv)

    print 'Making contours in figure ...'
    figure(figsize=(10,10))
    subplot(111,aspect=(1.0/cos(mean(lat)*pi/180.0)))
    levels = linspace(MinVal, MaxVal, num=NumberOfSamples)
    print 'Calling tricontourf  ...'
    contour = tricontourf(tri, var,levels=levels,shading='faceted')
    colorbar(orientation='horizontal')
    title(url)
    # This takes the axis limit string arg and converts it to a list. Then it converts that list to floats.
    if AxisLims != []:
        AxisLimsSplit = AxisLims.split(', ')
        AxisLims = map(float, AxisLimsSplit)
        axis(AxisLims)

    # Uncomment to show matplotlib visualization.
    # show()

    print "Saving figure as " +  imagefilename
    savefig(imagefilename)

    print 'Extracting contour shapes from tricontourf object ...'
    geoms = []
    # create list of tuples (geom, vmin, vmax)
    for colli,coll in enumerate(contour.collections):
        vmin,vmax = contour.levels[colli:colli+2]
        for p in coll.get_paths():
            p.simplify_threshold = 0.0
            polys = p.to_polygons()
            # Don't append an empty polygon to the geometry or it will screw up the indexing.
            if polys:
                geoms.append( (Polygon(polys[0],polys[1:] ),vmin,vmax))

    print "Writing shapes to " + shapefilename
    schema = { 'geometry': 'Polygon', 'properties': { 'vmin': 'float', 'vmax': 'float' } }
    with fiona.open(shapefilename, 'w', 'ESRI Shapefile', schema) as c:
        for geom in geoms:
            c.write({
                'geometry': mapping(geom[0]),
                'properties': {'vmin': geom[1], 'vmax': geom[2]},
            })

    print "Writing prj to " + prjfilename
    prj_string = '''GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'''
    prj_file = open(prjfilename, 'w')
    prj_file.write(prj_string)
    prj_file.close()

    # try reading the Shapefile back in 
    c = fiona.open(shapefilename, 'r')

if __name__ == "__main__":
    main(sys.argv[1:])
