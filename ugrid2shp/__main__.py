#! /usr/bin/env python

"""
A __main__ namespace for the ugrid2shp package.
"""

import sys
from ugrid2shp import ugrid2shp

if __name__ == '__main__':
    ugrid2shp(sys.argv[1:])
