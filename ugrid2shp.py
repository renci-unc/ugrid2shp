###
### ugrid2shp.py -  shapefile generator for CF-UGRID compliant netCDF files
###
### Idea from Rusty Holleman and Rich Signell (shapely/fiona)
### Code by Brian Blanton, RENCI
### 

from pylab import *
import matplotlib.tri as Tri
from shapely.geometry import mapping, Polygon
import fiona
import netCDF4
import datetime
import time
import sys
import getopt


def usage():
	print ' '
	print 'ugrid2shp.py -h -s -w -n <ncfilename> -o <outfile> -v <NcVariableName> -a <MinVal> -b <MaxVal> -c <NumLevels> -l <AxisLims> -t <TimeStepNum>'
	print '		'		
	print '	where:	-h | --Help				the text you are looking at right now'
	print '		-n | --Ncfilename	<ncfilename> 	netCDF file to read from, or a URL to an OPeNDAP file [maxele.63.nc]'
	print '		-o | --Outfile		<outfilename> 	filename to write shapefile to [outShape]'
	print '		-w | --WriteImage			write matplotlib image to a file <outfile>.png [False]'
	print '		-x | --ShowImage			display matplotlib image, user must close before continuing [False]'
	print '		-v | --NcVarName	<NcVarName> 	netCDF variable name to render [zeta_max]'
	print '		-a | --MinVal		<min value> 	smallest scalar value to render [0]'
	print '		-b | --MaxVal		<max value> 	largest scalar value to render [10]'
	print '		-c | --NumLevels	<num levels> 	number of contour levels [11]'
	print '		-l | --AxisLims		<[x0 y0 x1 y1]> axis limits to clip to [full domain]'
	print '		-t | --TimeStepNum	<time index> 	time step to render, in a time-domain file [1]'
	print '		-s | --Silent				no screen diagnostic output [True]'
	print ' '
	print '	A projection file (prj) is written containing the following:'
	print '		GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
	print '	To specify a different projection string, pass in -p | --ProjStr <projstr>, where projstr is as in this example:'
	print '		--ProjStr \'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]\' '
	print ' '
	

def main(argv):
    
    # Default parameter values.
    ncfilename='maxele.63.nc'
    outfile='outShape'
    NcVarName='zeta_max'
    MinVal = 0
    MaxVal = 10
    AxisLims = []
    NumLevels = 11
    Silent = True
    WriteImage = False
    ShowImage = False
    Tflag = False
    ProjStr='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'

    try:
        opts, args = getopt.getopt(argv,"hswxn:o:v:a:b:c:l:t:p:",["Help","Silent","WriteImage","Ncfilename=","Outfile=", "NcVariableName=", "MinVal=", "MaxVal=", "NumberOfSamples=", "AxisLims=", "TimeStepNum=","ProStr="])
    except getopt.GetoptError:
        print '\nUnrecognized command line option. '
        usage()
        sys.exit(2)
    for opt, arg in opts:
		if opt in ("-h", "--Help"):
			usage()
			sys.exit(2)
		elif opt in ("-s", "--Silent"):
			Silent = False
		elif opt in ("-w", "--WriteImage"):
			WriteImage = True
		elif opt in ("-x", "--ShowImage"):
			ShowImage = True
		elif opt in ("-t", "--TimeStepNum"):
			Tflag = True
			TimeStepNum = int(arg)
		elif opt in ("-n", "--Ncfilename"):
			ncfilename = arg
		elif opt in ("-o", "--Outfile"):
			outfile = arg
		elif opt in ("-v", "--NcVarName"):
			NcVarName = arg
		elif opt in ("-a", "--MinVal"):
			MinVal = float(arg)
		elif opt in ("-b", "--MaxVal"):
			MaxVal = float(arg)
		elif opt in ("-c", "--NumLevels"):
			NumLevels = int(arg)
		elif opt in ("-l", "--AxisLims"):
			AxisLims = arg     
		elif opt in ("-p", "--ProjStr"):
			ProjStr = arg     

    imagefilename=outfile+'.png'
    shapefilename=outfile+'.shp'
    prjfilename=outfile+'.prj'

    if ncfilename == None:
        raise Exception("You must pass a netCDF4 filename as an argument. Use the -n or --ncfilename argument to do this.")
        
    url = ncfilename
    #titl='ADCIRC';

    if url[-3:] != '.nc':
        url=url+'.nc'
    
    if not Silent == True : print 'Getting data from %s... ' % url
	    
    nc=netCDF4.Dataset(url).variables
    if not Silent == True : print nc.keys()
	    
    lon = nc['x'][:]
    lat = nc['y'][:]
    var = nc[NcVarName][:]
    nv = nc['element'][:,:]-1  # Move to 0-indexing by subtracting 1
	
    if not Silent == True:
    	print "Shape of lon is (%i)" % lon.shape
    	print "Shape of lat is (%i)" % lat.shape
    	print "Shape of nv is (%i, %i)" % nv.shape
    	print "Max of lon is (%i)" % lon.max()
    	print "Max of lat is (%i)" % lat.max()
    	print "Max of nv is (%i)" % nv.max()

    if Tflag == True:
        start=datetime.datetime(2008, 9, 13, 6, 0, 0)
        time_var = nc['time']
        print "The time chosen is: "
        print time_var[TimeStepNum]
        print "Units are: "
        print time_var.units
        if "since" in time_var.units:
            since_when = time_var.units.rsplit(None, 1)[-1]
            since_when_string = eval("time_var."+since_when)
            print since_when + " is " + since_when_string
        var = nc[NcVarName][TimeStepNum,:]
    
    if not Silent : print "First value in var: " + str(var[0])
		
    if not Silent == True : print 'Triangulating ...'
    tri = Tri.Triangulation(lon,lat, triangles=nv)

    if not Silent == True : print 'Making contours in figure ...'
    figure(figsize=(10,10))
    subplot(111,aspect=(1.0/cos(mean(lat)*pi/180.0)))
    levels = linspace(MinVal, MaxVal, num=NumLevels)
    
    if not Silent == True : print 'Calling tricontourf  ...'
    contour = tricontourf(tri, var,levels=levels,shading='faceted')
    colorbar(orientation='horizontal')
    title(url)
    
    # This takes the axis limit string arg and converts it to a list. Then it converts that list to floats.
    if AxisLims != []:
        AxisLimsSplit = AxisLims.split(', ')
        AxisLims = map(float, AxisLimsSplit)
        axis(AxisLims)

	if ShowImage == True: show()

    if WriteImage:
    	if not Silent == True : print "Saving figure as " +  imagefilename
    	savefig(imagefilename)

    if not Silent == True : print 'Extracting contour shapes from tricontourf object ...'
    
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

    if not Silent == True : print "Writing shapes to " + shapefilename
    
    schema = { 'geometry': 'Polygon', 'properties': { 'vmin': 'float', 'vmax': 'float' } }
    with fiona.open(shapefilename, 'w', 'ESRI Shapefile', schema) as c:
        for geom in geoms:
            c.write({
                'geometry': mapping(geom[0]),
                'properties': {'vmin': geom[1], 'vmax': geom[2]},
            })

    if not Silent == True : print "Writing prj to " + prjfilename
    
    prj_file = open(prjfilename, 'w')
    prj_file.write(ProjStr)
    prj_file.close()

    # try reading the Shapefile back in 
    #c = fiona.open(shapefilename, 'r')

if __name__ == "__main__":
    main(sys.argv[1:])
