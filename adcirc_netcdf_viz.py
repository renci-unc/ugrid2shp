from pylab import *

import matplotlib.tri as Tri
from shapely.geometry import mapping, Polygon
import fiona
import netCDF4
import datetime
import time
import sys



imagefilename='test.png'
shapefilename='test.shp'
titl='ADCIRC';
url='twm_example.nc'
#url='http://opendap.renci.org:1935/thredds/dodsC/ASGS/andrea/08/nc6b/blueridge.renci.org/fivemem/nhcConsensus/maxele.63.nc'
# url = sys.argv[1]
vname='maxele'
#vname='zeta'
#vname='zeta_max'
# vname=sys.argv[2]
start=datetime.datetime(2008, 9, 13, 6, 0, 0)

# print 'Getting data from url ... '
print 'Getting data from twm_example.nc ... '

time0=time.time()
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
print 'elapsed time= %d seconds' % (time.time()-time0)
print "var[0]: " + str(var[0])

print 'Triangulating ...'
time0=time.time()
tri = Tri.Triangulation(lon,lat, triangles=nv)
print 'elapsed time= %d seconds' % (time.time()-time0)

print 'Making contours in figure ...'
time0=time.time()
figure(figsize=(10,10))
subplot(111,aspect=(1.0/cos(mean(lat)*pi/180.0)))
levels = linspace(0.,5.,11)
print 'Calling tricontourf  ...'
contour = tricontourf(tri, var,levels=levels,shading='faceted')
colorbar(orientation='horizontal')
title(url)
print 'elapsed time= %d seconds' % (time.time()-time0)


# show()

print "Saving figure as " +  imagefilename
savefig(imagefilename)

time0=time.time()
print 'Extracting contour shapes from tricontourf object ...'
geoms = []
# create list of tuples (geom, vmin, vmax)
for colli,coll in enumerate(contour.collections):
    vmin,vmax = contour.levels[colli:colli+2]
    for p in coll.get_paths():
        p.simplify_threshold = 0.0
        polys = p.to_polygons()
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
print 'elapsed time= %d seconds' % (time.time()-time0)

# try reading the Shapefile back in 
c = fiona.open(shapefilename, 'r')