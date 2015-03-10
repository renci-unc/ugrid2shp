import sys
sys.path.append("")
import ugrid2shp
import unittest


class TestParseArgs(unittest.TestCase):
    defaults = {'ProjStr': 'GEOGCS["GCS_WGS_1984",'
                           'DATUM["D_WGS_1984",'
                           'SPHEROID["WGS_1984",6378137.0,298.257223563]],'
                           'PRIMEM["Greenwich",0.0],'
                           'UNIT["Degree",0.0174532925199433]]',
                'axis_limits': [],
                'debug': False,
                'maxval': 10,
                'minval': 0,
                'nc_var_name': 'zeta_max',
                'ncfilename': 'maxele.63.nc',
                'no_zip': False,
                'numlevels': 11,
                'outfilename': 'outShape',
                'show_image': False,
                'silent': False,
                'write_image': False}

    def test_defaults(self):
        args = vars(ugrid2shp.parse_args([]))
        self.assertEqual(self.defaults, args)

if __name__ == "__main__":
    unittest.main()
