"""
$ python netcdf_viz.py -n  http://opendap.renci.org:1935/thredds/dodsC/ASGS/andrea/08/nc6b/blueridge.renci.org/fivemem/nhcConsensus/maxele.63.nc -o test_thredds -v zeta_max -a 0 -b 11
Getting data from url=http://opendap.renci.org:1935/thredds/dodsC/ASGS/andrea/08/nc6b/blueridge.renci.org/fivemem/nhcConsensus/maxele.63.nc...
[u'time', u'x', u'y', u'element', u'adcirc_mesh', u'neta', u'nvdll', u'_nc4_non_coord_max_nvdll', u'ibtypee', u'nbdv', u'nvel', u'nvell', u'_nc4_non_coord_max_nvell', u'ibtype', u'nbvv', u'depth', u'zeta_max']
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

"""
if __name__ == '__main__':
	import shelldoctest
	shelldoctest.testmod(verbose=3)