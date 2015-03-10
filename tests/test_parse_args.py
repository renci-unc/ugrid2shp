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

    def test_d_arg(self):
        args = vars(ugrid2shp.parse_args("-d".split()))
        self.assertEqual(args['debug'], True,
                         "Option -d did not set debug argument to True")

    def test_debug_arg(self):
        args = vars(ugrid2shp.parse_args("--debug".split()))
        self.assertEqual(args['debug'], True,
                         "Option --debug did not set debug argument to True")

    def test_s_arg(self):
        args = vars(ugrid2shp.parse_args("-s".split()))
        self.assertEqual(args['silent'], True,
                         "Option -s did not set silent argument to True")

    def test_silent_arg(self):
        args = vars(ugrid2shp.parse_args("--silent".split()))
        self.assertEqual(args['silent'], True,
                         "Option --silent did not set silent argument to True")

    def test_w_arg(self):
        args = vars(ugrid2shp.parse_args("-w".split()))
        self.assertEqual(args['write_image'], True,
                         "Option -w did not set write_image argument to True")

    def test_writeimage_arg(self):
        args = vars(ugrid2shp.parse_args("--writeimage".split()))
        self.assertEqual(args['write_image'], True,
                         "Option --writeimage "
                         "did not set write_image argument to True")

    def test_x_arg(self):
        args = vars(ugrid2shp.parse_args("-x".split()))
        self.assertEqual(args['show_image'], True,
                         "Option -s did not set show_image argument to True")

    def test_showimage_arg(self):
        args = vars(ugrid2shp.parse_args("--showimage".split()))
        self.assertEqual(args['show_image'], True,
                         "Option --showimage "
                         "did not set show_image argument to True")

    def test_z_arg(self):
        args = vars(ugrid2shp.parse_args("-z".split()))
        self.assertEqual(args['no_zip'], True,
                         "Option -z did not set no_zip argument to True")

    def test_nozip_arg(self):
        args = vars(ugrid2shp.parse_args("--nozip".split()))
        self.assertEqual(args['no_zip'], True,
                         "Option --nozip did not set no_zip argument to True")

    def test_n_arg(self):
        test_ncfilename = "yipee"
        args = vars(ugrid2shp.parse_args(("-n %s"
                                          % (test_ncfilename)).split()))
        self.assertEqual(args['ncfilename'], test_ncfilename,
                         "Option -n "
                         "did not set provided filename '%s'"
                         % (test_ncfilename))

    def test_ncfilename_arg(self):
        test_ncfilename = "yikes"
        args = vars(ugrid2shp.parse_args(("--ncfilename %s"
                                          % (test_ncfilename)).split()))
        self.assertEqual(args['ncfilename'], test_ncfilename,
                         "Option -ncfilename "
                         "did not set provided filename '%s'"
                         % (test_ncfilename))

if __name__ == "__main__":
    unittest.main()
