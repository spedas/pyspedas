"""
Tests for cotrans functions.

These tests include the function in the following files:
    utilites/contrans.py
    utilities/cotrans_lib.py
    utilites/igrf.py
    utilites/j2000.py
    themis/cotrans/dsl2gse.py

"""
import unittest
import pyspedas
from pyspedas.themis.cotrans.dsl2gse import dsl2gse
from pyspedas.utilities.cotrans import cotrans
from pytplot import get_data, del_data


class CotransTestCases(unittest.TestCase):
    """Tests for cotrans."""

    def test_dsl2gse(self):
        """Test themis.cotrans.dsl2gse."""
        del_data()
        # Try with missing variables. It should exit without problems.
        dsl2gse('tha_fgl_dsl', 'tha_spinras', 'tha_spindec', 'tha_fgl_gse')
        # Now load the needed variables.
        time_range = ['2017-03-23 00:00:00', '2017-03-23 23:59:59']
        pyspedas.themis.state(probe='a', trange=time_range,
                              get_support_data=True,
                              varnames=['tha_spinras', 'tha_spindec'])
        pyspedas.themis.fgm(probe='a', trange=time_range,
                            varnames=['tha_fgl_dsl'])

        dsl2gse('tha_fgl_dsl', 'tha_spinras', 'tha_spindec', 'tha_fgl_gse')

        t, d = get_data('tha_fgl_gse')
        # Now test the inverse.
        dsl2gse('tha_fgl_dsl', 'tha_spinras', 'tha_spindec', 'tha_fgl_gse',
                isgsetodsl=1)

        self.assertTrue(abs(d[0].tolist()[0]-15.905078404701147) <= 1e-6)
        self.assertTrue(abs(d[0].tolist()[1]--13.962618931740064) <= 1e-6)
        self.assertTrue(abs(d[0].tolist()[2]-16.392516225582813) <= 1e-6)

        self.assertTrue(abs(d[50000].tolist()[0]-16.079111468932435) <= 1e-6)
        self.assertTrue(abs(d[50000].tolist()[1]--18.858874541698583) <= 1e-6)
        self.assertTrue(abs(d[50000].tolist()[2]-14.75796300561617) <= 1e-6)

    def test_cotrans(self):
        """Test cotrans.py GEI->GEO with Themis data."""
        del_data()
        trange = ['2010-02-25/00:00:00', '2010-02-25/23:59:59']
        probe = 'a'
        name_in = "tha_pos"
        name_out = "tha_pos_new_geo"
        pyspedas.themis.state(probe=probe, trange=trange,
                              time_clip=True, varnames=[name_in])
        cotrans(name_in=name_in, name_out=name_out,
                coord_in="gei", coord_out="geo")
        din = get_data(name_in)
        in_len = len(din[0])
        dout = get_data(name_out)
        out_len = len(dout[0])
        cotrans(name_in=name_in, coord_in="gei", coord_out="geo")
        self.assertTrue(out_len == in_len)

    def test_cotrans_igrf(self):
        """Test GSE->GSM and IGRF."""
        del_data()
        d = [[245.0, -102.0, 251.0], [775.0, 10.0, -10],
             [121.0, 545.0, -1.0], [304.65, -205.3, 856.1],
             [464.34, -561.55, -356.22]]
        t = [1577112800, 1577308800, 1577598800, 1577608800, 1577998800]
        name_out = "tname_out"
        cotrans(name_out=name_out, time_in=t, data_in=d,
                coord_in="gse", coord_out="gsm")
        in_len = len(t)
        dout = get_data(name_out)
        out_len = len(dout[0])
        gsm = dout[1][1]
        res = [775.0, 11.70325822, -7.93937951]
        self.assertTrue(out_len == in_len)
        self.assertTrue(abs(gsm[0]-res[0]) <= 1e-6)
        self.assertTrue(abs(gsm[1]-res[1]) <= 1e-6)
        self.assertTrue(abs(gsm[2]-res[2]) <= 1e-6)

    def test_cotrans_j2000(self):
        """Test GEI->J2000 and J2000 params."""
        del_data()
        d = [[245.0, -102.0, 251.0], [775.0, 10.0, -10],
             [121.0, 545.0, -1.0], [304.65, -205.3, 856.1],
             [464.34, -561.55, -356.22]]
        t = [1577112800, 1577308800, 1577598800, 1577608800, 1577998800]
        name_out = "tname_out"
        cotrans(name_out=name_out, time_in=t, data_in=d,
                coord_in="gei", coord_out="j2000")
        in_len = len(t)
        dout = get_data(name_out)
        out_len = len(dout[0])
        j2000 = dout[1][1]
        res = [775.01595209, 6.59521058, -11.47942543]
        self.assertTrue(out_len == in_len)
        self.assertTrue(abs(j2000[0]-res[0]) <= 1e-6)
        self.assertTrue(abs(j2000[1]-res[1]) <= 1e-6)
        self.assertTrue(abs(j2000[2]-res[2]) <= 1e-6)

    def test_cotrans_geigsm(self):
        """Test daisy chain of multiple transofrmations, GEI->GSE->GSM."""
        del_data()
        d = [[245.0, -102.0, 251.0], [775.0, 10.0, -10],
             [121.0, 545.0, -1.0], [304.65, -205.3, 856.1],
             [464.34, -561.55, -356.22]]
        t = [1577112800, 1577308800, 1577598800, 1577608800, 1577998800]
        name_out = "tname_out"
        cotrans(name_out=name_out, time_in=t, data_in=d,
                coord_in="gei", coord_out="gsm")
        in_len = len(t)
        dout = get_data(name_out)
        out_len = len(dout[0])
        gsm = dout[1][1]
        res = [4.59847513e+01, 7.62303493e+02, 1.32679267e+02]
        self.assertTrue(out_len == in_len)
        self.assertTrue(abs(gsm[0]-res[0]) <= 1e-6)
        self.assertTrue(abs(gsm[1]-res[1]) <= 1e-6)
        self.assertTrue(abs(gsm[2]-res[2]) <= 1e-6)

    def test_all_cotrans(self):
        """Test all cotrans pairs.

        Apply transformation, then inverse transformation and compare.
        """
        cotrans()
        all_cotrans = ['gei', 'geo', 'j2000', 'gsm', 'mag', 'gse', 'sm']
        d = [[245.0, -102.0, 251.0], [775.0, 10.0, -10],
             [121.0, 545.0, -1.0], [304.65, -205.3, 856.1],
             [464.34, -561.55, -356.22]]
        dd1 = d[1]
        t = [1577112800, 1577308800, 1577598800, 1577608800, 1577998800]
        in_len = len(t)
        name1 = "name1"
        name2 = "name2"
        count = 0
        # Test non-existent system.
        cotrans(name_out=name1, time_in=t, data_in=d,
                coord_in="coord_in", coord_out="coord_out")
        # Test empty data.
        cotrans(name_out=name1, time_in=t, data_in=[],
                coord_in="gei", coord_out="geo")
        cotrans(time_in=t, data_in=d, coord_in="gse", coord_out="gsm")
        # Test all combinations.
        for coord_in in all_cotrans:
            for coord_out in all_cotrans:
                count += 1
                del_data()
                cotrans(name_out=name1, time_in=t, data_in=d,
                        coord_in=coord_in, coord_out=coord_out)
                dout = get_data(name1)
                out_len1 = len(dout[0])
                self.assertTrue(out_len1 == in_len)
                # Now perform inverse transformation.
                cotrans(name_in=name1, name_out=name2,
                        coord_in=coord_out, coord_out=coord_in)
                dout2 = get_data(name2)
                out_len2 = len(dout2[0])
                dd2 = dout2[1][1]
                print(count, "--- in:", coord_in, "out:", coord_out)
                # print(dout[1][1])
                # print(dd2)
                self.assertTrue(out_len2 == in_len)
                self.assertTrue(abs(dd1[0]-dd2[0]) <= 1e-6)
                self.assertTrue(abs(dd1[1]-dd2[1]) <= 1e-6)
                self.assertTrue(abs(dd1[2]-dd2[2]) <= 1e-6)


if __name__ == '__main__':
    unittest.main()
