###
### ugrid2shp.py -  shapefile generator for CF-UGRID compliant netCDF files
###
### Idea from Rusty Holleman and Rich Signell (shapely/fiona)
### Code by Brian Blanton, RENCI
### 

from pylab import *
import matplotlib.tri as Tri
import matplotlib.pyplot as plt
from shapely.geometry import mapping, Polygon
import fiona
import netCDF4
import datetime
import time
import sys
import getopt
import zipfile
import os

def usage():
	print '\nUsage:\n'
#	print 'ugrid2shp.py -h -d -s -w -x -z -n <NcFileName|url> -o <OutFile> -v <NcVariableName> -a <MinVal> -b <MaxVal> -c <NumLevels> -l <AxisLims> -t <TimeStepNum> -p <ProjectionString>'
	print 'ugrid2shp.py -h -d -s -w -x -z -n <NcFileName|url> -o <OutFile> -v <NcVariableName> -a <MinVal> -b <MaxVal> -c <NumLevels> -l <AxisLims> -p <ProjectionString>'
	print '		'		
	print '	where:	-h | --Help				the text you are looking at right now'
	print '		-d | --Debug				display debugging diagnostics [False]'
	print '		-s | --Silent				no screen diagnostic output [True]'
	print '		-w | --WriteImage			write matplotlib image to a file <outfile>.png [False]'
	print '		-x | --ShowImage			display matplotlib image, user must close before continuing [False]'
	print '		-z | --NoZip				no zip file output [False]'
	print '		-n | --NcFileName	<ncfilename> 	netCDF file to read from, or a URL to an OPeNDAP file [maxele.63.nc]'
	print '		-o | --OutFile		<outfilename> 	filename to write shapefile to [outShape]'
	print '		-v | --NcVarName	<NcVarName> 	netCDF variable name to render [zeta_max]'
	print '		-a | --MinVal		<min value> 	smallest scalar value to render [0]'
	print '		-b | --MaxVal		<max value> 	largest scalar value to render [10]'
	print '		-c | --NumLevels	<num levels> 	number of contour levels [11]'
	print '		-l | --AxisLims		<[x0 y0 x1 y1]> axis limits to clip to [full domain]'
#	print '		-t | --TimeStepNum	<time index> 	time step index to render, in a time-domain file [1]'
	print '		-p | --ProjStr				Projection string for prj file;  see below.'
	print ' '
	print '	A projection file (prj) is written containing the following:'
	print '		GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
	print '	To specify a different projection string, pass in -p | --ProjStr <projstr>, where projstr is as in this example:'
	print '		--ProjStr \'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]\' '
	print ' '
	print ' Test URLs: '
	print ' 	Coarse resolution ADCIRC grid: '
	print ' 		http://opendap.renci.org:1935/thredds/dodsC/ASGS/nam/2013112112/ec95d/hatteras.renci.org/cfsamp/namforecast/maxele.63.nc'
	print ' 	Medium resolution ADCIRC grid: '
	print ' 		http://opendap.renci.org:1935/thredds/dodsC/ASGS/andrea/08/nc6b/blueridge.renci.org/fivemem/nhcConsensus/maxele.63.nc'
	print ' '
	

def main(argv):
    
    # Default parameter values.
    ncfilename='maxele.63.nc'
    outfilename='outShape'
    NcVarName='zeta_max'
    MinVal = 0
    MaxVal = 10
    AxisLims = []
    NumLevels = 11
    Silent = False
    WriteImage = False
    ShowImage = False
    WriteZip = True
    Tflag = False
    Debug = False
    ProjStr='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'

    try:
        opts, args = getopt.getopt(argv,"hdswxzn:o:v:a:b:c:l:t:p:",["Help","Silent","WriteImage","NoZip","Debug","NcFileName=","OutFile=", "NcVariableName=", "MinVal=", "MaxVal=", "NumberOfSamples=", "AxisLims=", "TimeStepNum=","ProjStr="])
    except getopt.GetoptError as err:
        print '\nCommand line option error: ' + str(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
		if opt in ("-h", "--Help"):
			usage()
			sys.exit(2)
		elif opt in ("-s", "--Silent"):
			Silent = True
		elif opt in ("-z", "--NoZip"):
			WriteZip = False
		elif opt in ("-w", "--WriteImage"):
			WriteImage = True
		elif opt in ("-x", "--ShowImage"):
			ShowImage = True
		elif opt in ("-d", "--Debug"):
			Debug = True
		elif opt in ("-t", "--TimeStepNum"):
			Tflag = True
			TimeStepNum = int(arg)
		elif opt in ("-n", "--NcFileName"):
			ncfilename = arg
		elif opt in ("-o", "--OutFileName"):
			outfilename = arg
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

    imagefilename =outfilename+'.png'
    shapefilename =outfilename+'.shp'
    prjfilename   =outfilename+'.prj'
    zipfilename   =outfilename+'.zip'
    readmefilename='README.txt'

    # get timestamp
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if Debug == True : print "Create time " + st

    if ncfilename == None:
        raise Exception("You must pass a netCDF filename or url as an argument. Use the -n or --NcFileName argument to do this.")
        
    url = ncfilename
    path,file  = os.path.split(url)
    if not path : path='file://'
    if not Silent == True : print path+file

    # end of url must have .nc 
    # if url[-3:] != '.nc': url=url+'.nc'
    
    # get stuff from netCDF file
    if not Silent == True : print 'Getting data from %s... ' % url
	    
    nc=netCDF4.Dataset(url)
    vars=nc.variables
    if Debug == True : print vars.keys()
	
    # get some global attributes
    model=getattr(nc,'model')
    grid=getattr(nc,'agrid')
    inst=getattr(nc,'institution')

    # print out all global attributes
    #for name in nc.ncattrs():
    #    print 'Global attr', name, '=', getattr(nc,name)
	
    lon = vars['x'][:]
    lat = vars['y'][:]
    var = vars[NcVarName]
    units=var.units
    data = vars[NcVarName][:]
    elems = vars['element'][:,:]-1  # Move to 0-indexing by subtracting 1
    titl='MatPlotLib plot of ' + NcVarName + ' in ' + file 
	
    if Debug == True:
    	print "\n   Shape of lon is (%i)" % lon.shape
    	print "   Shape of lat is (%i)" % lat.shape
    	print "   Shape of nv is (%i, %i)" % elems.shape
    	print "   Max of lon is (%i)" % lon.max()
    	print "   Max of lat is (%i)" % lat.max()
    	print "   Max of nv is (%i)" % elems.max()
    	print "   First value in var: " + str(data[0]) + '\n'

#     if Tflag == True:
#         start=datetime.datetime(2008, 9, 13, 6, 0, 0)
#         time_var = nc['time']
#         print "The time chosen is: "
#         print time_var[TimeStepNum]
#         print "Units are: "
#         print time_var.units
#         if "since" in time_var.units:
#             since_when = time_var.units.rsplit(None, 1)[-1]
#             since_when_string = eval("time_var."+since_when)
#             print since_when + " is " + since_when_string
#         var = nc[NcVarName][TimeStepNum,:]
    	
    if not Silent == True : print 'Triangulating ...'
    tri = Tri.Triangulation(lon,lat, triangles=elems)

    if not Silent == True : print 'Making contours in figure ...'
    fig=plt.figure(figsize=(10,10))
    plt.subplot(111,aspect=(1.0/cos(mean(lat)*pi/180.0)))
    levels = linspace(MinVal, MaxVal, num=NumLevels)
    
    if not Silent == True : print 'Calling tricontourf  ...'
    contour = tricontourf(tri, data,levels=levels,shading='faceted')
    cbar=fig.colorbar(contour,orientation='vertical',ticks=levels)
    cbar.set_label(units)
    title(titl)
    figtext(.5,.05,'URL: '+path+file,size='small',horizontalalignment='center')
    
    # This takes the axis limit string arg and converts it to a list. Then it converts that list to floats.
    if AxisLims != []:
        AxisLimsSplit = AxisLims.split(',')
        AxisLims = map(float, AxisLimsSplit)
        axis(AxisLims)

    if WriteImage:
    	if not Silent == True : print "Saving figure as " +  imagefilename
    	savefig(imagefilename)

    if ShowImage:
		print "\nDisplay window must be closed before shapefile can be written. \n"
		show()

    # this is the meat, as per Rusty Holleman
    if not Silent == True : print 'Extracting contour shapes from tricontourf object ...'
    geoms = []
    for colli,coll in enumerate(contour.collections):  # create list of tuples (geom, vmin, vmax)
        vmin,vmax = contour.levels[colli:colli+2]
        for p in coll.get_paths():
            p.simplify_threshold = 0.0
            polys = p.to_polygons()
            # Don't append an empty polygon to the geometry or it will screw up the indexing.
            if polys:
                # Don't append holes without at least three coordinates
                polys[1:] = [poly for poly in polys[1:] if poly.shape[0] > 2]
                geoms.append( (Polygon(polys[0],polys[1:] ),vmin,vmax))

    # this is the other meat, as per Rusty Holleman
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

	# write a README file
    rmf=open(readmefilename,mode='w')
    rmf.write('CreateTime : '+st+'\n')
    rmf.write('Model : '+model+'\n')
    rmf.write('Grid : '+grid+'\n')
    rmf.write('Institution : '+inst+'\n')
    rmf.write('Url : '+path+'\n')
    rmf.write('File : '+file+'\n')
    rmf.write('ProjStr : '+ProjStr+'\n')
    rmf.write('Units : '+units+'\n')
    rmf.close()
		
    if WriteZip == True:
		if not Silent == True : print 'Flushing zip file to ' +  zipfilename
		zf=zipfile.ZipFile(zipfilename,mode='w')
		zf.write(outfilename+'.shp')
		if os.path.isfile(outfilename+'.prj') : zf.write(outfilename+'.prj')
		if os.path.isfile(outfilename+'.cpg') : zf.write(outfilename+'.cpg')
		if os.path.isfile(outfilename+'.shx') : zf.write(outfilename+'.shx')
		if os.path.isfile(outfilename+'.dbf') : zf.write(outfilename+'.dbf')
		zf.write(readmefilename)
		zf.close()
		if os.path.isfile(outfilename+'.prj') : os.remove(outfilename+'.prj')
		if os.path.isfile(outfilename+'.cpg') : os.remove(outfilename+'.cpg')
		if os.path.isfile(outfilename+'.shx') : os.remove(outfilename+'.shx')
		if os.path.isfile(outfilename+'.dbf') : os.remove(outfilename+'.dbf')
		os.remove(outfilename+'.shp')		
	
    # try reading the Shapefile back in 
    #c = fiona.open(shapefilename, 'r')

if __name__ == "__main__":
    main(sys.argv[1:])
