import unittest

import numpy as np

import pyspedas
from pyspedas import (
    data_exists,
    time_double,
    tinterpol,
    join_vec,
    store_data,
    get_data,
    tdeflag,
    del_data,
    set_coords,
    set_units,
)
from pyspedas.geopack import tt89, tt96, tt01, tts04, tigrf
from pyspedas.geopack.get_tsy_params import get_tsy_params
from pyspedas.geopack.get_w_params import get_w

trange = ["2018-10-16", "2018-10-17"]


def gen_circle_alt():
    # Generate a circle at 5 RE in the XZ plane
    angle = np.arange(0.0, 361.0, 1.0)
    angle_rad = np.deg2rad(angle)
    y = np.zeros(len(angle_rad), np.float64)
    x = 5.0 * np.sin(angle_rad) * 6371.2
    z = 5.0 * np.cos(angle_rad) * 6371.2
    t = np.zeros(len(angle_rad))
    t[:] = time_double("2018-10-16/06:31:00") + np.arange(0.0, 361.0, 1.0)
    pos = np.zeros((len(angle_rad), 3), np.float64)
    pos[:, 0] = x
    pos[:, 1] = y
    pos[:, 2] = z
    store_data("circle_magpoles_5re", data={"x": t, "y": pos})
    set_coords("circle_magpoles_5re", "GSM")
    set_units("circle_magpoles_5re", 'km')


def get_params(model, g_variables=None):
    support_trange = [
        time_double(trange[0]) - 60 * 60 * 24,
        time_double(trange[1]) + 60 * 60 * 24,
    ]
    pyspedas.projects.kyoto.dst(trange=support_trange)
    pyspedas.projects.omni.data(trange=trange)
    join_vec(["BX_GSE", "BY_GSM", "BZ_GSM"])
    if model == "t01" and g_variables is None:
        g_variables = [6.0, 10.0]
    else:
        if g_variables is not None:
            if not isinstance(g_variables, str) and not isinstance(
                g_variables, np.ndarray
            ):
                g_variables = None
    return get_tsy_params(
        "kyoto_dst",
        "BX_GSE-BY_GSM-BZ_GSM_joined",
        "proton_density",
        "flow_speed",
        model,
        pressure_tvar="Pressure",
        g_variables=g_variables,
        speed=True,
    )


class LoadTestCases(unittest.TestCase):


    #@unittest.skip("Download site for w parameters is offline")
    def test_tts04(self):
        mec_vars = pyspedas.projects.mms.mec(trange=trange)
        self.assertTrue(mec_vars)
        params = get_params("ts04")
        tinterpol("mms1_mec_r_gsm", "proton_density")
        tts04("mms1_mec_r_gsm-itrp", parmod=params)
        self.assertTrue(data_exists("mms1_mec_r_gsm-itrp_bts04"))

    #@unittest.skip("Download site for w parameters is offline")
    def test_get_w(self):
        w_vals = get_w(trange=trange)
        self.assertTrue(w_vals)

    #@unittest.skip("Download site for w parameters is offline")
    def test_t04_roi(self):
        gen_circle_alt()
        params = get_params("ts04")
        dat = get_data(params)
        circ_dat = get_data("circle_magpoles_5re")
        n = len(circ_dat.times)
        newdat = np.zeros((n, 10), np.float64)
        newdat[:, :] = dat.y[0,]
        store_data(params, data={"x": circ_dat.times, "y": newdat})
        tts04("circle_magpoles_5re", parmod=params)
        # pyspedas.tplot(['circle_magpoles_5re','circle_magpoles_5re_bts04'])


if __name__ == "__main__":
    unittest.main()
