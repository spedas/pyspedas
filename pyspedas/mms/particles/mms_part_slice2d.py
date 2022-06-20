import pyspedas
from pyspedas import time_double
from pyspedas.mms.fpi.mms_get_fpi_dist import mms_get_fpi_dist
from pyspedas.mms.hpca.mms_get_hpca_dist import mms_get_hpca_dist
from pyspedas.particles.spd_slice2d.slice2d import slice2d
from pyspedas.particles.spd_slice2d.slice2d_plot import plot


def mms_part_slice2d(trange=None,
                     time=None,
                     samples=None,
                     window=None,
                     center_time=False,
                     erange=None,
                     energy=False,
                     log=False,
                     probe='1',
                     instrument='fpi',
                     data_rate=None,
                     level='l2',
                     mag_data_rate=None,
                     species=None,
                     rotation='xy',
                     custom_rotation=None,
                     subtract_bulk=False,
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

    if trange is None:
        if time is None:
            print('Please specify a time or time range over which to compute the slice.')
            return
        trange_data = [time_double(time)-60, time_double(time)+60]
    else:
        trange_data = trange

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
    probe = str(probe)

    if rotation in ['xy', 'xz', 'yz']:
        load_support = False
    else:
        load_support = True

    if subtract_bulk:
        load_support = True

    if instrument == 'fpi':
        # not supposed to be centered!
        dist_vars = pyspedas.mms.fpi(probe=probe, trange=trange_data, data_rate=data_rate, time_clip=True,
                                     datatype='d' + species + 's-dist', level=level)

        dists = mms_get_fpi_dist('mms' + probe + '_d' + species + 's_dist_' + data_rate, probe=probe)
    elif instrument == 'hpca':
        # supposed to be centered!
        dist_vars = pyspedas.mms.hpca(probe=probe, trange=trange_data, data_rate=data_rate, time_clip=True,
                                      datatype='ion', level=level, center_measurement=True)

        dists = mms_get_hpca_dist('mms' + probe + '_hpca_' + species + '_phase_space_density', species=species,
                                  probe=probe, data_rate=data_rate)
    else:
        print('Unknown instrument: ' + instrument + '; valid options: fpi, hpca')
        return

    bfield = None
    vbulk = None
    if load_support:
        fgm_support = pyspedas.mms.fgm(probe=probe, trange=trange_data, data_rate=mag_data_rate, time_clip=True)
        bfield = 'mms' + probe + '_fgm_b_gse_' + mag_data_rate + '_l2_bvec'

        if instrument == 'fpi':
            fpi_support = pyspedas.mms.fpi(probe=probe, trange=trange_data, data_rate=data_rate, time_clip=True,
                                           datatype='d'+species+'s-moms', level=level, center_measurement=True)
            vbulk = 'mms' + probe + '_d' + species + 's_bulkv_gse_' + data_rate
        elif instrument == 'hpca':
            hpca_support = pyspedas.mms.hpca(probe=probe, trange=trange_data, data_rate=data_rate, time_clip=True,
                                             datatype='moments', level=level, center_measurement=True)
            vbulk = 'mms' + probe + '_hpca_' + species + '_ion_bulk_velocity'

    the_slice = slice2d(dists, trange=trange, time=time, window=window, samples=samples, center_time=center_time,
                        mag_data=bfield, vel_data=vbulk, rotation=rotation, resolution=resolution, erange=erange,
                        energy=energy, log=log, custom_rotation=custom_rotation, subtract_bulk=subtract_bulk)

    plot(the_slice, xrange=xrange, yrange=yrange, zrange=zrange, save_png=save_png, save_svg=save_svg,
         save_pdf=save_pdf, save_eps=save_eps, display=display)
