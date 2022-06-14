import pyspedas
from pyspedas.mms.fpi.mms_get_fpi_dist_slice2d import mms_get_fpi_dist_slice2d
from pyspedas.particles.spd_slice2d.slice2d import slice2d
from pyspedas.particles.spd_slice2d.slice2d_plot import plot


def mms_part_slice2d(trange=None,
                     probe='1',
                     instrument='fpi',
                     data_rate=None,
                     level='l2',
                     mag_data_rate=None,
                     species=None,
                     rotation='xy',
                     xrange=None,
                     yrange=None,
                     zrange=None,
                     resolution=500,
                     save_png=None,
                     save_svg=None,
                     save_pdf=None,
                     save_eps=None,
                     display=True):
    """
    EXPERIMENTAL, PLEASE DO NOT USE
    """

    if species is None:
        if instrument == 'fpi':
            species = 'e'
        else:
            species = 'hplus'

    if data_rate is None:
        if instrument == 'fpi':
            data_rate = 'fast'
        else:
            data_rate = 'srvy'

    if mag_data_rate is None:
        if data_rate == 'brst':
            mag_data_rate = 'brst'
        else:
            mag_data_rate = 'srvy'

    instrument = instrument.lower()
    data_rate = data_rate.lower()
    level = level.lower()

    if instrument == 'fpi':
        # not supposed to be centered!
        pyspedas.mms.fpi(probe=probe, trange=trange, data_rate=data_rate, time_clip=True,
                         datatype=['d' + species + 's-dist', 'd' + species + 's-moms'],
                         level=level)

        dists = mms_get_fpi_dist_slice2d('mms' + probe + '_d' + species + 's_dist_' + data_rate, probe=probe)

    pyspedas.mms.fgm(probe=probe, trange=trange, data_rate=mag_data_rate, time_clip=True)

    bfield = 'mms' + probe + '_fgm_b_gse_' + mag_data_rate + '_l2_bvec'
    vbulk = 'mms' + probe + '_d' + species + 's_bulkv_gse_' + data_rate

    s = slice2d(dists, trange=trange, mag_data=bfield, vel_data=vbulk, rotation=rotation)

    plot(s, xrange=xrange, yrange=yrange, zrange=zrange, save_png=save_png, save_svg=save_svg,
         save_pdf=save_pdf, save_eps=save_eps, display=display)