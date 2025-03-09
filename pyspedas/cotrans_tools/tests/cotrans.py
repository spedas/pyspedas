"""
Tests for cotrans_tools functions.

These tests include the function in the following files:
    utilites/contrans.py
    utilities/cotrans_lib.py
    utilites/igrf.py
    utilites/j2000.py
    themis/cotrans_tools/dsl2gse.py

"""
import numpy as np
import unittest
import pyspedas
import logging
from pyspedas.projects.themis.cotrans.dsl2gse import dsl2gse
from pyspedas.cotrans_tools.cotrans import cotrans
from pyspedas.cotrans_tools.fac_matrix_make import fac_matrix_make
from pytplot import get_data, store_data, del_data
from pyspedas import cotrans_get_coord, cotrans_set_coord, sm2mlt, tplot_copy, set_units, get_units


class CotransTestCases(unittest.TestCase):
    """Tests for cotrans."""

    def test_fac_matrix_make(self):
        with self.assertLogs(level='ERROR') as log:
            doesntexist = fac_matrix_make('doesnt_exist')
            self.assertTrue(doesntexist is None)
            self.assertIn("Error reading tplot variable: doesnt_exist", log.output[0])

    def test_get_set_coord_wrappers(self):
        """ Test for cotrans_set_coord/cotrans_get_coord wrappers """
        del_data()
        doesntexist = cotrans_get_coord('test_coord')
        self.assertTrue(doesntexist is None)
        store_data('test_coord', data={'x': [1, 2, 3, 4, 5], 'y': [1, 1, 1, 1, 1]})
        with self.assertLogs(level='ERROR') as log:
            cotrans(name_in='test_coord', coord_out="geo")
            self.assertIn("cotrans error: No input coordinates were provided.", log.output[0])
        before = cotrans_get_coord('test_coord')
        self.assertTrue(before is None)
        setcoord = cotrans_set_coord('test_coord', 'GSE')
        self.assertTrue(setcoord)
        after = cotrans_get_coord('test_coord')
        self.assertTrue(after == 'GSE')
        md = get_data('test_coord', metadata=True)
        md['data_att']['units'] = 'km'
        setcoord = cotrans_set_coord('test_coord', 'GSM')
        self.assertTrue(setcoord)
        md_after = get_data('test_coord', metadata=True)
        after = cotrans_get_coord('test_coord')
        self.assertTrue(after == 'GSM')
        self.assertTrue(md_after['data_att']['units'] == 'km')
        setcoord = cotrans_set_coord('doesnt_exist', 'GSM')

    def test_get_set_coords(self):
        """ Test for pytplot.set_coords/get_coords """
        from pytplot import set_coords, get_coords

        del_data()
        doesntexist = get_coords('test_coord')
        self.assertTrue(doesntexist is None)   
        store_data('test_coord', data={'x': [1, 2, 3, 4, 5], 'y': [1, 1, 1, 1, 1]})
        with self.assertLogs(level='ERROR') as log:
            cotrans(name_in='test_coord', coord_out="geo")
            self.assertIn("cotrans error: No input coordinates were provided.", log.output[0])
        before = get_coords('test_coord')
        self.assertTrue(before is None)
        setcoord = set_coords('test_coord', 'GSE')
        self.assertTrue(setcoord)
        after = get_coords('test_coord')
        self.assertTrue(after == 'GSE')
        md = get_data('test_coord', metadata=True)
        md['data_att']['units'] = 'km'
        setcoord = set_coords('test_coord', 'GSM')
        self.assertTrue(setcoord)
        md_after = get_data('test_coord', metadata=True)
        after = get_coords('test_coord')
        self.assertTrue(after == 'GSM')
        self.assertTrue(md_after['data_att']['units'] == 'km')
        setcoord = set_coords('doesnt_exist', 'GSM')

    def test_get_set_units(self):
        """ Test for pytplot.set_coords/get_coords """
        from pytplot import set_units, get_units, set_coords, get_coords

        del_data()
        doesntexist = get_units('test_units')
        self.assertTrue(doesntexist is None)
        store_data('test_units', data={'x': [1, 2, 3, 4, 5], 'y': [1, 1, 1, 1, 1]})
        before = get_units('test_units')
        self.assertTrue(before is None)
        setunits = set_units('test_units', 'Km')
        self.assertTrue(setunits)
        after = get_units('test_units')
        self.assertTrue(after == 'Km')
        set_coords('test_units', 'GEO')
        setunits = set_units('test_units', 'mm')
        self.assertTrue(setunits)
        coords_after = get_coords('test_units')
        units_after = get_units('test_units')
        self.assertTrue(coords_after == 'GEO')
        self.assertTrue(units_after == 'mm')

    def test_dsl2gse(self):
        """Test themis.cotrans_tools.dsl2gse."""
        del_data()
        # Try with missing variables. It should exit without problems.
        with self.assertLogs(level='ERROR') as log:
            dsl2gse('tha_fgl_dsl', 'tha_fgl_gse')
            self.assertIn("Variables needed: ['tha_fgl_dsl']", log.output[0])
            self.assertIn("Variables missing: ['tha_fgl_dsl']", log.output[1])
            self.assertIn("Please load missing variables.", log.output[2])
        # Now load the needed variables.
        time_range = ['2017-03-23 00:00:00', '2017-03-23 23:59:59']
        pyspedas.projects.themis.state(probe='a', trange=time_range,
                              get_support_data=True,
                              varnames=['tha_spinras', 'tha_spindec'])
        pyspedas.projects.themis.fgm(probe='a', trange=time_range,
                            varnames=['tha_fgl_dsl'])

        fac_matrix_make('tha_fgl_dsl')

        dsl2gse('tha_fgl_dsl', 'tha_fgl_gse')

        t, d = get_data('tha_fgl_gse')
        # Now test the inverse.
        dsl2gse('tha_fgl_dsl', 'tha_fgl_gse',
                isgsetodsl=True)

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
        pyspedas.projects.themis.state(probe=probe, trange=trange,
                              time_clip=True, varnames=[name_in])
        cotrans(name_in=name_in, name_out=name_out,
                coord_in="gei", coord_out="geo")
        din = get_data(name_in)
        in_len = len(din[0])
        dout = get_data(name_out)
        out_len = len(dout[0])
        cotrans(name_in=name_in, coord_in="gei", coord_out="geo")
        self.assertTrue(out_len == in_len)

    def test_cotrans_coord_mismatch(self):
        """Test that cotrans rejects a request where in_coord does not match the system from the variable metadata."""
        del_data()
        trange = ['2010-02-25/00:00:00', '2010-02-25/23:59:59']
        probe = 'a'
        name_in = "tha_pos"
        name_out = "tha_pos_new_geo"
        pyspedas.projects.themis.state(probe=probe, trange=trange,
                              time_clip=True, varnames=[name_in])
        # Metadata coordinate system is GEI, but requesting GSM->GEO transform.  This should generate an error message
        # and return failure.
        with self.assertLogs(level='ERROR') as log:
            result = cotrans(name_in=name_in, name_out=name_out,
                            coord_in="gsm", coord_out="geo")
            self.assertTrue(result == 0)

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
        res = [775.0, 11.70357713,-7.93890939]
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
        res = [ 45.98475132, 762.29816225, 132.7098884 ]
        self.assertTrue(out_len == in_len)
        self.assertTrue(abs(gsm[0]-res[0]) <= 1e-6)
        self.assertTrue(abs(gsm[1]-res[1]) <= 1e-6)
        self.assertTrue(abs(gsm[2]-res[2]) <= 1e-6)

    def test_all_cotrans(self):
        """Test all cotrans pairs.

        Apply transformation, then inverse transformation and compare.
        """
        with self.assertLogs(level='ERROR') as log:
            cotrans()
            self.assertIn("cotrans error: No output coordinates were provided.", log.output[0])
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
        # Test non-existent systems.
        with self.assertLogs(level='ERROR') as log:
            result = cotrans(name_out=name1, time_in=t, data_in=d,
                            coord_in="badcoord", coord_out="gei")
            self.assertTrue(result == 0)
            self.assertIn("cotrans error: Requested input coordinate system", log.output[0])
            result = cotrans(name_out=name1, time_in=t, data_in=d,
                            coord_in="gei", coord_out="badcoord")
            self.assertTrue(result == 0)
            self.assertIn("cotrans error: Requested output coordinate system", log.output[1])

        # Test empty data.
        with self.assertLogs(level='ERROR') as log:
            cotrans(name_out=name1, time_in=t, data_in=[],
                    coord_in="gei", coord_out="geo")
            cotrans(time_in=t, data_in=d, coord_in="gse", coord_out="gsm")
            self.assertIn("cotrans error: Data is empty.", log.output[0])
            self.assertEqual(len(log.output), 1)
        # Test all combinations.
        with self.assertLogs(level='WARNING') as log:
            for i, coord_in in enumerate(all_cotrans):
                for j, coord_out in enumerate(all_cotrans):
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
                    logging.info("%d --- in: %s out: %s", count, coord_in, coord_out)
                    # print(dout[1][1])
                    # print(dd2)
                    self.assertTrue(out_len2 == in_len)
                    self.assertTrue(abs(dd1[0]-dd2[0]) <= 1e-6)
                    self.assertTrue(abs(dd1[1]-dd2[1]) <= 1e-6)
                    self.assertTrue(abs(dd1[2]-dd2[2]) <= 1e-6)
                    if coord_out == coord_in:
                        self.assertIn("Warning: coord_in equal to coord_out.", log.output[i*2])
                        self.assertIn("Warning: coord_in equal to coord_out.", log.output[j*2+1])
                

    def test_mlt(self):
        '''Test sm2mlt.

        Data is from goes18, 2023-01-01. [0, 100, 600, 1000]
        '''

        # SM coordinates and MLT values from IDL
        sm_idl = [[33199.660, 25815.376, 2995.6487], [18814.747, 37614.243, 2990.7136],
                  [-40428.563, -11607.452, 2995.3227], [15798.372, -38974.509, 2995.0028]]
        mlt_idl = [14.524527, 16.228377, 1.0679544, 7.4710163]

        x = [item[0] for item in sm_idl]
        y = [item[1] for item in sm_idl]
        z = [item[2] for item in sm_idl]

        mlt_python = sm2mlt(x, y, z)

        for i in range(4):
            self.assertTrue(abs(mlt_idl[i]-mlt_python[i]) <= 1e-6)

    def test_units_coords(self):
        '''Test setting units and coordinate systems (including wildcards)
        '''

        test_dat = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        test_times = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

        store_data('v1', data={'x':test_times, 'y':test_dat})
        tplot_copy('v1', 'v2')
        tplot_copy('v1', 'v3')
        tplot_copy('v1','v4')

        cotrans_set_coord('v?', 'GSE')
        c1 = cotrans_get_coord('v1')
        c2 = cotrans_get_coord('v2')
        c3 = cotrans_get_coord('v3')
        c4 = cotrans_get_coord('v4')
        self.assertTrue(c1 == 'GSE')
        self.assertTrue(c2 == 'GSE')
        self.assertTrue(c3 == 'GSE')
        self.assertTrue(c4 == 'GSE')

        set_units('v?', 'nT')
        u1 = get_units('v1')
        u2 = get_units('v2')
        u3 = get_units('v3')
        u4 = get_units('v4')
        self.assertTrue(u1 == 'nT')
        self.assertTrue(u2 == 'nT')
        self.assertTrue(u3 == 'nT')
        self.assertTrue(u4 == 'nT')

        res = cotrans_set_coord('nonexistent', 'GSE')
        self.assertFalse(res)

        res = set_units('xxx yyy zzz', 'nT')
        self.assertFalse(res)

if __name__ == '__main__':
    unittest.main()
