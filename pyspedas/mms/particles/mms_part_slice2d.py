import logging
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
                     thetarange=None,
                     zdirrange=None,
                     average_angle=None,
                     sum_angle=None,
                     energy=False,
                     log=False,
                     probe='1',
                     instrument='fpi',
                     data_rate=None,
                     level='l2',
                     spdf=False,
                     mag_data_rate=None,
                     species=None,
                     rotation='xy',
                     custom_rotation=None,
                     subtract_bulk=False,
                     xrange=None,
                     yrange=None,
                     zrange=None,
                     resolution=None,
                     interpolation='geometric',
                     contours=False,
                     smooth=None,
                     save_jpeg=None,
                     save_png=None,
                     save_svg=None,
                     save_pdf=None,
                     save_eps=None,
                     plotsize=10,
                     dpi=None,
                     return_slice=False,
                     cmap=None,
                     display=True):
    """
    This routine creates 2D slices of 3D distribution function data from the FPI and HPCA instruments.
    This is essentially a wrapper around slice2d and slice2d_plot, that loads the data,
    any required support data, calculates the slice with slice2d and plots it with slice2d_plot.

    Parameters
    -----------
        probe: int or str
            MMS spacecraft probe # (1, 2, 3 or 4)

        instrument: str
            MMS plasma instrument (fpi or hpca)

        species: str
            Particle species; depends on the instrument:
            FPI: 'e' for electrons, 'i' for ions
            HPCA: 'hplus' for H+, 'oplus' for O+, 'heplus' for He+, 'heplusplus', for He++

        data_rate: str
            FPI/HPCA data rate [fast (fpi), srvy (hpca), or brst (both fpi and hpca)]

        mag_data_rate: str
            FGM data rate for transformations

        level: str
            Data level (default: l2); lower levels require an SDC username and password

        spdf: bool
            Flag to download the data from SPDF instead of the MMS SDC

        trange: list of str or list of float
            Two-element time range over which data will be averaged (optional; can also use the 'time' keyword)

        time: str or float
            Time at which the slice will be computed (optional; can also use 'trange' above)

        samples: int
            Number of nearest samples to TIME to average.

        window: float
            Length in seconds from TIME over which data will be averaged

        center_time: bool
            Flag denoting that TIME should be midpoint for window instead of beginning

        interpolation: str
            Interpolation method; valid options:

            'geometric': Each point on the plot is given the value of the bin it intersects.
                         This allows bin boundaries to be drawn at high resolutions.
            '2d': Data points within the specified theta or z-axis range are projected onto
                  the slice plane and linearly interpolated onto a regular 2D grid.

        rotation: str
            Aligns the data relative to the magnetic field and/or bulk velocity.
            This is applied after the CUSTOM_ROTATION. (BV and BE are invariant
            between coordinate systems); valid options:

            'BV':  The x axis is parallel to B field; the bulk velocity defines the x-y plane
            'BE':  The x axis is parallel to B field; the B x V(bulk) vector defines the x-y plane
            'xy':  (default) The x axis is along the data's x axis and y is along the data's y axis
            'xz':  The x axis is along the data's x axis and y is along the data's z axis
            'yz':  The x axis is along the data's y axis and y is along the data's z axis
            'xvel':  The x axis is along the data's x axis; the x-y plane is defined by the bulk velocity
            'perp':  The x axis is the bulk velocity projected onto the plane normal to the B field; y is B x V(bulk)
            'perp_xy':  The data's x & y axes are projected onto the plane normal to the B field
            'perp_xz':  The data's x & z axes are projected onto the plane normal to the B field
            'perp_yz':  The data's y & z axes are projected onto the plane normal to the B field

        custom_rotation: str or np.ndarray
            Applies a custom rotation matrix to the data.  Input may be a
            3x3 rotation matrix or a tplot variable containing matrices.
            If the time window covers multiple matrices they will be averaged.
            This is applied before other transformations

        energy: bool
            Flag to plot data against energy (in eV) instead of velocity.

        log: bool
            Flag to apply logarithmic scaling to the radial measure (i.e. energy/velocity).
            (on by default if ENERGY is True)

        erange: list of float
            Two element array specifying the energy range to be used in eV

        thetarange: list of float
            (2D interpolation only) Angle range, in degrees [-90,90], used to calculate slice.
            Default = [-20,20]; will override ZDIRRANGE.

        zdirrange: list of float
            (2D interpolation only) Z-Axis range, in km/s, used to calculate slice.
            Ignored if called with THETARANGE.

        subtract_bulk: bool
            Subtract the bulk velocity vector

        resolution: int
            Integer specifying the resolution along each dimension of the
            slice (defaults:  2D interpolation: 150, geometric: 500)

        smooth: int
            An odd integer >=3 specifying the width of a smoothing window in #
            of points.  Smoothing is applied to the final plot using a gaussian
            convolution. Even entries will be incremented, 0 and 1 are ignored.

        xrange: list of float
            Keyword to limit the range of the slice's x-axis in the plot

        yrange: list of float
            Keyword to limit the range of the slice's y-axis in the plot

        zrange: list of float
            Keyword to limit the range of the slice's color bar

        save_png: str
            Save the plot as a PNG file

        save_eps: str
            Save the plot as an EPS file

        save_pdf: str
            Save the plot as a PDF file

        save_svg: str
            Save the plot as an SVG file

        display: bool
            Flag to allow disabling displaying of the figure

        return_slice: bool
            Flag to return the slice instead of displaying it

    Returns
    --------
        None (but creates a figure), unless return_slice is set to True

    """

    if trange is None:
        if time is None:
            logging.error('Please specify a time or time range over which to compute the slice.')
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
                                     datatype='d' + species + 's-dist', level=level, spdf=spdf)

        dists = mms_get_fpi_dist('mms' + probe + '_d' + species + 's_dist_' + data_rate, probe=probe)
    elif instrument == 'hpca':
        # supposed to be centered!
        dist_vars = pyspedas.mms.hpca(probe=probe, trange=trange_data, data_rate=data_rate, time_clip=True,
                                      datatype='ion', level=level, center_measurement=True, spdf=spdf)

        dists = mms_get_hpca_dist('mms' + probe + '_hpca_' + species + '_phase_space_density', species=species,
                                  probe=probe, data_rate=data_rate)
    else:
        logging.error('Unknown instrument: ' + instrument + '; valid options: fpi, hpca')
        return

    bfield = None
    vbulk = None
    if load_support:
        fgm_support = pyspedas.mms.fgm(probe=probe, trange=trange_data, data_rate=mag_data_rate, time_clip=True, spdf=spdf)
        bfield = 'mms' + probe + '_fgm_b_gse_' + mag_data_rate + '_l2_bvec'

        if instrument == 'fpi':
            fpi_support = pyspedas.mms.fpi(probe=probe, trange=trange_data, data_rate=data_rate, time_clip=True,
                                           datatype='d'+species+'s-moms', level=level, center_measurement=True, spdf=spdf)
            vbulk = 'mms' + probe + '_d' + species + 's_bulkv_gse_' + data_rate
        elif instrument == 'hpca':
            hpca_support = pyspedas.mms.hpca(probe=probe, trange=trange_data, data_rate=data_rate, time_clip=True,
                                             datatype='moments', level=level, center_measurement=True, spdf=spdf)
            vbulk = 'mms' + probe + '_hpca_' + species + '_ion_bulk_velocity'

    the_slice = slice2d(dists, trange=trange, time=time, window=window, samples=samples, center_time=center_time,
                        mag_data=bfield, vel_data=vbulk, rotation=rotation, resolution=resolution, erange=erange,
                        energy=energy, log=log, custom_rotation=custom_rotation, subtract_bulk=subtract_bulk,
                        interpolation=interpolation, thetarange=thetarange, zdirrange=zdirrange, smooth=smooth,
                        average_angle=average_angle, sum_angle=sum_angle)

    if return_slice:
        return the_slice

    plot(the_slice, xrange=xrange, yrange=yrange, zrange=zrange, save_png=save_png, save_svg=save_svg,
         save_pdf=save_pdf, save_eps=save_eps, save_jpeg=save_jpeg, display=display, dpi=dpi, plotsize=plotsize,
         contours=contours, colormap=cmap)
