import ugrid2shp
import unittest


class TestParseArgs(unittest.TestCase):
    def test_defaults(self):
        args = vars(ugrid2shp.parse_args([]))
        self.assertEqual(ugrid2shp.defaults, args)

    def test_d_arg(self):
        args = vars(ugrid2shp.parse_args("-d".split()))
        self.assertEqual(args['debug'],
                         not ugrid2shp.defaults['debug'],
                         "Option -d did not turn on debug mode.")

    def test_debug_arg(self):
        args = vars(ugrid2shp.parse_args("--debug".split()))
        self.assertEqual(args['debug'],
                         not ugrid2shp.defaults['debug'],
                         "Option --debug did not turn one debug mode.")

    def test_s_arg(self):
        args = vars(ugrid2shp.parse_args("-s".split()))
        self.assertEqual(args['silent'],
                         not ugrid2shp.defaults['silent'],
                         "Option -s did not turn on silent mode.")

    def test_silent_arg(self):
        args = vars(ugrid2shp.parse_args("--silent".split()))
        self.assertEqual(args['silent'],
                         not ugrid2shp.defaults['silent'],
                         "Option --silent did not turn on silent mode.")

    def test_w_arg(self):
        args = vars(ugrid2shp.parse_args("-w".split()))
        self.assertEqual(args['write_image'],
                         not ugrid2shp.defaults['write_image'],
                         "Option -w did not turn on image writing.")

    def test_writeimage_arg(self):
        args = vars(ugrid2shp.parse_args("--writeimage".split()))
        self.assertEqual(args['write_image'],
                         not ugrid2shp.defaults['write_image'],
                         "Option --writeimage did not turn on image writing.")

    def test_x_arg(self):
        args = vars(ugrid2shp.parse_args("-x".split()))
        self.assertEqual(args['show_image'],
                         not ugrid2shp.defaults['show_image'],
                         "Option -s did not turn on image display.")

    def test_showimage_arg(self):
        args = vars(ugrid2shp.parse_args("--showimage".split()))
        self.assertEqual(args['show_image'],
                         not ugrid2shp.defaults['show_image'],
                         "Option --showimage did not turn on image display.")

    def test_z_arg(self):
        args = vars(ugrid2shp.parse_args("-z".split()))
        self.assertEqual(args['no_zip'],
                         not ugrid2shp.defaults['no_zip'],
                         "Option -z did not turn off zip file output.")

    def test_nozip_arg(self):
        args = vars(ugrid2shp.parse_args("--nozip".split()))
        self.assertEqual(args['no_zip'],
                         not ugrid2shp.defaults['no_zip'],
                         "Option --nozip did not turn off zip file output.")

    def test_n_arg(self):
        test_ncfilename = "yipee.nc"
        args = vars(ugrid2shp.parse_args(("-n %s"
                                          % (test_ncfilename)).split()))
        self.assertEqual(args['ncfilename'],
                         test_ncfilename,
                         "Option -n did not set filename.")

    def test_ncfilename_arg(self):
        test_ncfilename = "yikes.nc"
        args = vars(ugrid2shp.parse_args(("--ncfilename %s"
                                          % (test_ncfilename)).split()))
        self.assertEqual(args['ncfilename'],
                         test_ncfilename,
                         "Option --ncfilename did not set filename.")

if __name__ == "__main__":
    unittest.main()
