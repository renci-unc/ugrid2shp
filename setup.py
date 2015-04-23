from setuptools import setup, \
                       find_packages

setup(name='pyugrid',
      version='1.0',
      packages=find_packages(),
      author='Brian O. Blanton',
      author_email='bblanton@renci.org',
      description='Compute GIS shapefiles '
                  'from a CF-UGRID compliant netCDF file.',
      keywords="UGRID CF NetCDF shapefile",
      url="https://github.com/renci-unc/ugrid2shp",
      test_suite="ugrid2shp.tests")
