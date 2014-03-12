#!/usr/local/bin/python
"""
$ python netcdf_viz.py -n twm_example -o test_local -v maxele_prediction -a 0 -b 11 -s '-82, -72, 29, 39'
Getting data from url=twm_example.nc...
[u'x', u'y', u'maxele', u'maxele_prediction', u'element', u'bnd']
Shape of lon is (608114)
Shape of lat is (608114)
Shape of nv is (1200767, 3)
Max of lon is (-60)
Max of lat is (45)
Max of nv is (608113)
var[0]: -99999.0
Triangulating ...
Making contours in figure ...
Calling tricontourf  ...
Saving figure as test_local.png
Extracting contour shapes from tricontourf object ...
Writing shapes to test_local.shp
Writing prj to test_local.prj

"""
if __name__ == '__main__':
	import shelldoctest
	shelldoctest.testmod(verbose=3)