
import pyspedas
from pyspedas.themis.cotrans.dsl2gse import dsl2gse
from pytplot import get_data

class CotransTestCases(unittest.TestCase):
    def test_dsl2gse(self):
        time_range = ['2017-03-23 00:00:00', '2017-03-23 23:59:59']
        pyspedas.themis.state(probe='a', trange=time_range, get_support_data=True, varnames=['tha_spinras', 'tha_spindec'])
        pyspedas.themis.fgm(probe='a', trange=time_range, varnames=['tha_fgl_dsl'])

        dsl2gse('tha_fgl_dsl', 'tha_spinras', 'tha_spindec', 'tha_fgl_gse')

        t, d = get_data('tha_fgl_gse')

        self.assertTrue(d[0].tolist()[0]-15.905078404701147 <= 1e-6)
        self.assertTrue(d[0].tolist()[1]--13.962618931740064 <= 1e-6)
        self.assertTrue(d[0].tolist()[2]-16.392516225582813 <= 1e-6)

        self.assertTrue(d[50000].tolist()[0]-16.079111468932435 <= 1e-6)
        self.assertTrue(d[50000].tolist()[1]--18.858874541698583 <= 1e-6)
        self.assertTrue(d[50000].tolist()[2]-14.75796300561617 <= 1e-6)