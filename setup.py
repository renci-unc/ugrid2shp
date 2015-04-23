from setuptools import setup
from setuptools import find_packages


def version():
    """Get the version number."""

    with open("VERSION.txt") as v:
        _version = v.read()
    return _version.strip()


__version__ = version()


def long_description():
    """Construct the long description text."""

    with open("README.rst") as r:
        long_description_1 = r.read()
    with open("HISTORY.txt") as h:
        long_description_2 = h.read()
    return "\n".join([long_description_1, long_description_2, ])


setup(name='ugrid2shp',
      version=__version__,
      license="GPL2",
      packages=find_packages(),
      author='Brian O. Blanton',
      author_email='bblanton@renci.org',
      description='Compute a GIS shapefile '
                  'from a CF-UGRID compliant netCDF file.',
      long_description=long_description(),
      url="https://github.com/renci-unc/ugrid2shp",
      keywords="UGRID CF NetCDF shapefile",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "License :: OSI Approved :: "
                   "GNU General Public License v2 (GPLv2)",
                   "Programming Language :: Python :: 2.7",
                   "Topic :: Scientific/Engineering :: Atmospheric Science",
                   "Topic :: Scientific/Engineering :: GIS", ],
      zip_safe=False,
      test_suite="ugrid2shp.tests")
