import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pytplot
from pytplot import get_data
import pyspedas
from pyspedas import time_double
from pyspedas.mms.fpi.mms_get_fpi_dist import mms_get_fpi_dist


def mms_fpi_ang_ang(time,
                    species='i',
                    probe='1',
                    data_rate='fast',
                    level='l2',
                    center_measurement=False,
                    energy_range=[10, 30000],
                    xsize=8,
                    ysize=8,
                    cmap='spedas',
                    zrange=[None, None],
                    display=True):
    """
    Creates various plots directly from the FPI distribution functions, including:
         - angle-angle (azimuth vs zenith)
         - angle-energy (azimuth and zenith vs energy)

    Input
    ------
        time: str
            Time to generate the angle-angle plots for

    Parameters
    -----------
        species: str
            'i' for ions, 'e' for electrons

        probe: str
            MMS spacecraft probe # (1-4)

        data_rate: str
            Data rate ('brst' or 'fast')

        level: str
            Data level

        center_measurement: bool
            Flag to center the FPI measurements

        energy_range: list
            Range of energies to include in the figures (default: 10-30000 eV)

        xsize: float
            X-size of the output figure

        ysize: float
            Y-size of the output figure

        cmap: str
            Color map to use (default: 'spedas')

        zrange: list
            Range of the color bar

        display: bool
            Flag to display the figures (with plt.show()); default: True

    """

    trange = [time_double(time)-300, time_double(time)+300]

    fpi_vars = pyspedas.mms.fpi(trange=trange,
                                datatype=['d'+species+'s-moms', 'd'+species+'s-dist'],
                                probe=probe,
                                data_rate=data_rate,
                                level=level,
                                center_measurement=center_measurement)

    dist = get_data('mms'+probe+'_d'+species+'s_dist_'+data_rate)

    closest_idx = np.searchsorted(dist.times, time_double(time), side='left')

    data = dist.y[closest_idx, :, :, :]

    if len(dist.v1.shape) > 1:
        phi = dist.v1[closest_idx, :]
    else:
        phi = dist.v1

    theta = dist.v2
    energies = dist.v3[closest_idx, :]
    energy_axis = [np.nanmin(energies), np.nanmax(energies)]

    idx_of_ens = np.argwhere((energies >= energy_range[0]) & (energies <= energy_range[1])).flatten()
    energies = energies[idx_of_ens]
    data_at_ens = data[:, :, idx_of_ens]
    data_summed = np.nansum(data_at_ens, axis=2)

    dists = mms_get_fpi_dist('mms'+probe+'_d'+species+'s_dist_'+data_rate,
                             single_time=time)

    # theta is stored as co-latitude
    theta_colat = dists[0]['theta'][0, 0, :]

    # convert to latitude
    theta_flow_direction = 90.0 - theta_colat
    phi = dists[0]['phi'][0, :, 0]

    spec_options = {}

    # the first figure: azimuth vs. zenith
    fig, axes = plt.subplots()
    fig.set_size_inches(xsize, ysize)

    # add support for the 'spedas' color bar
    if cmap == 'spedas':
        _colors = pytplot.spedas_colorbar
        spd_map = [(np.array([r, g, b])).astype(np.float64)/256 for r, g, b in zip(_colors.r, _colors.g, _colors.b)]
        spec_options['cmap'] = LinearSegmentedColormap.from_list('spedas', spd_map)
    else:
        spec_options['cmap'] = cmap

    # phi can be out of order, so we need to sort prior to sending to pcolormesh
    phi_sorted_idx = np.argsort(phi)
    phi_sorted = phi[phi_sorted_idx]
    data_phi_sorted = data_summed[phi_sorted_idx, :]

    spec_options['norm'] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])

    im = axes.pcolormesh(phi_sorted, theta_flow_direction, data_phi_sorted.T, **spec_options)

    axes.set_xlabel('Az flow angle (deg)')
    axes.set_ylabel('Zenith flow angle (deg)')
    fig.subplots_adjust(left=0.14, right=0.85)
    box = axes.get_position()
    pad, width = 0.02, 0.02
    cax = fig.add_axes([box.xmax + pad, box.ymin, width, box.height])
    colorbar = fig.colorbar(im, cax=cax)
    colorbar.set_label('f ($s^3$/$cm^6$)')

    # Zenith vs. energy
    fig2, axes2 = plt.subplots()
    fig2.set_size_inches(xsize, ysize)

    theta_en = np.nansum(data_at_ens, axis=0)

    axes2.set_xscale('log')
    axes2.set_xlabel('Energy (eV)')
    axes2.set_ylabel('Zenith flow angle (deg)')
    fig2.subplots_adjust(left=0.14, right=0.85)

    zrange_is_None = zrange[0] is None

    if zrange_is_None:
        zrange[0] = np.nanmin(theta_en[theta_en > 0])

    spec_options['norm'] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])

    im2 = axes2.pcolormesh(energies, theta_flow_direction, theta_en, **spec_options)

    cax2 = fig2.add_axes([box.xmax + pad, box.ymin, width, box.height])
    colorbar2 = fig2.colorbar(im2, cax=cax2)
    colorbar2.set_label('f ($s^3$/$cm^6$)')

    # Azimuth vs. energy
    fig3, axes3 = plt.subplots()
    fig3.set_size_inches(xsize, ysize)

    phi_en = np.nansum(data_at_ens[phi_sorted_idx, :, :], axis=1)

    fig3.subplots_adjust(left=0.14, right=0.85)
    axes3.set_xscale('log')
    axes3.set_xlabel('Energy (eV)')
    axes3.set_ylabel('Azimuth flow angle (deg)')

    if zrange_is_None:
        zrange[0] = np.nanmin(phi_en[phi_en > 0])

    spec_options['norm'] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])

    im3 = axes3.pcolormesh(energies, phi_sorted, phi_en, **spec_options)

    cax3 = fig3.add_axes([box.xmax + pad, box.ymin, width, box.height])
    colorbar3 = fig3.colorbar(im3, cax=cax3)
    colorbar3.set_label('f ($s^3$/$cm^6$)')

    if display:
        plt.show()
