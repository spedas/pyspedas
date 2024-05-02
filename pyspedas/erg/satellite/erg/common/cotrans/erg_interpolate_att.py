import numpy as np
from pytplot import tnames
from pytplot import tcrossp
from pytplot import time_string
from pytplot import get_data, get_timespan
from pytplot.tplot_math.degap import degap
from scipy import interpolate

from ...att.att import att


def erg_interpolate_att(erg_xxx_in=None, noload=False):
    """
    This function interpolates erg att data to match erg_xxx_in.

    Parameters:
        erg_xxx_in : str
            input tplot variable relating to ERG to be transformed

    Returns:
        output_dictionary : dict
            Dictionary which has below keys.
                spinperiod: output variable in which the interpolated data of ERG spin period is stored
                spinphase: output variable in which the interpolated data of ERG spin phase is stored
                sgix_j2000, sgiy_j2000, or sgiz_j2000: output interporated SGI axis vector for each component
                sgax_j2000, sgay_j2000, or sgaz_j2000: output interporated SGA axis vector for each component

    """
    if (erg_xxx_in is None) or (erg_xxx_in not in tnames()):
        print('inputted Tplot variable name is None, or not defined')
        return

    reload = not noload

    time_array = get_data(erg_xxx_in)[0]

    # Prepare some constants
    dtor = np.pi / 180.

    output_dictionary = {}

    # Load the attitude data
    if tnames('erg_att_sprate') == ['erg_att_sprate']:
        if reload:
            degap('erg_att_sprate', dt=8., margin=.5)
        sprate = get_data('erg_att_sprate')
        if sprate[0].min() > time_array.min() + 8. or sprate[0].max() < time_array.max() - 8.:
            tr = get_timespan(erg_xxx_in)
            if reload:
                att(trange=time_string([tr[0] - 60., tr[1] + 60.]))
    else:
        tr = get_timespan(erg_xxx_in)
        if reload:
            att(trange=time_string([tr[0] - 60., tr[1] + 60.]))

    # Interpolate spin period
    if reload:
        degap('erg_att_sprate', dt=8., margin=.5)
    sprate = get_data('erg_att_sprate')
    sper = 1. / (sprate[1] / 60.)
    sperInterp = np.interp(time_array, sprate[0], sper)
    spinperiod = {'x': time_array, 'y': sperInterp}
    output_dictionary['spinperiod'] = spinperiod

    # Interpolate spin phase
    if reload:
        degap('erg_att_spphase', dt=8., margin=.5)
    sphase = get_data('erg_att_spphase')
    if (sphase[0][0] <= time_array[0])\
            and (time_array[-1] <= sphase[0][-1]):
        ph_nn = interpolate.interp1d(
            sphase[0], sphase[1], kind="nearest")(time_array)
        dt = time_array - \
            interpolate.interp1d(sphase[0], sphase[0], kind="nearest")(time_array)
    elif (time_array[0] < sphase[0][0])\
            or (sphase[0][-1] < time_array)[-1]:
        ph_nn = interpolate.interp1d(
            sphase[0], sphase[1], kind="nearest", fill_value='extrapolate')(time_array)
        dt = time_array - \
            interpolate.interp1d(sphase[0], sphase[0], kind="nearest", fill_value='extrapolate')(time_array)

    per_nn = spinperiod['y']

    sphInterp = np.fmod(ph_nn + 360. * dt / per_nn, 360.)
    sphInterp = np.fmod(sphInterp + 360., 360.)
    spinphase = {'x': time_array, 'y': sphInterp}
    output_dictionary['spinphase'] = spinphase

    # Interporate SGI-Z axis vector
    if reload:
        degap('erg_att_izras', dt=8., margin=0.5)
        degap('erg_att_izdec', dt=8., margin=0.5)
    ras = get_data('erg_att_izras')
    dec = get_data('erg_att_izdec')
    time0 = ras[0]
    ras = ras[1]
    dec = dec[1]
    ez = np.cos((90. - dec) * dtor)
    ex = np.sin((90. - dec) * dtor) * np.cos(ras * dtor)
    ey = np.sin((90. - dec) * dtor) * np.sin(ras * dtor)
    ex_interp = np.interp(time_array, time0, ex)
    ey_interp = np.interp(time_array, time0, ey)
    ez_interp = np.interp(time_array, time0, ez)
    sgiz_j2000 = {'x': time_array, 'y': np.array(
        [ex_interp, ey_interp, ez_interp]).T}
    output_dictionary['sgiz_j2000'] = sgiz_j2000

    # Interporate SGA-X axis vector
    if reload:
        degap('erg_att_gxras', dt=8., margin=0.5)
        degap('erg_att_gxdec', dt=8., margin=0.5)
    ras = get_data('erg_att_gxras')
    dec = get_data('erg_att_gxdec')
    time0 = ras[0]
    ras = ras[1]
    dec = dec[1]
    ez = np.cos((90. - dec) * dtor)
    ex = np.sin((90. - dec) * dtor) * np.cos(ras * dtor)
    ey = np.sin((90. - dec) * dtor) * np.sin(ras * dtor)
    ex_interp = np.interp(time_array, time0, ex)
    ey_interp = np.interp(time_array, time0, ey)
    ez_interp = np.interp(time_array, time0, ez)
    sgax_j2000 = {'x': time_array, 'y': np.array(
        [ex_interp, ey_interp, ez_interp]).T}
    output_dictionary['sgax_j2000'] = sgax_j2000

    # Interporate SGA-Z axis vector
    if reload:
        degap('erg_att_gzras', dt=8., margin=0.5)
        degap('erg_att_gzdec', dt=8., margin=0.5)
    ras = get_data('erg_att_gzras')
    dec = get_data('erg_att_gzdec')
    time0 = ras[0]
    ras = ras[1]
    dec = dec[1]
    ez = np.cos((90. - dec) * dtor)
    ex = np.sin((90. - dec) * dtor) * np.cos(ras * dtor)
    ey = np.sin((90. - dec) * dtor) * np.sin(ras * dtor)
    ex_interp = np.interp(time_array, time0, ex)
    ey_interp = np.interp(time_array, time0, ey)
    ez_interp = np.interp(time_array, time0, ez)
    sgaz_j2000 = {'x': time_array, 'y': np.array(
        [ex_interp, ey_interp, ez_interp]).T}
    output_dictionary['sgaz_j2000'] = sgaz_j2000

    # Derive the other three axes (SGA-Y, SGI-X, SGI-Y)
    sgay = tcrossp(output_dictionary['sgaz_j2000']['y'],
                   output_dictionary['sgax_j2000']['y'], return_data=True)
    sgay_j2000 = {'x': time_array, 'y': sgay}
    output_dictionary['sgay_j2000'] = sgay_j2000

    sgiy = tcrossp(output_dictionary['sgiz_j2000']['y'],
                   output_dictionary['sgax_j2000']['y'], return_data=True)
    sgiy_j2000 = {'x': time_array, 'y': sgiy}
    output_dictionary['sgiy_j2000'] = sgiy_j2000

    sgix = tcrossp(output_dictionary['sgiy_j2000']['y'],
                   output_dictionary['sgiz_j2000']['y'], return_data=True)
    sgix_j2000 = {'x': time_array, 'y': sgix}
    output_dictionary['sgix_j2000'] = sgix_j2000

    return output_dictionary
