
import os
import matplotlib.pyplot as plt
from pytplot import get_data
from . import mms_load_mec

def mms_orbit_plot(trange=['2015-10-16', '2015-10-17'], probes=[1, 2, 3, 4], data_rate='srvy', xr=None, yr=None, plane='xy', coord='gse'):
    """
    This function creates MMS orbit plots
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: list of str
            probe #, e.g., '4' for MMS4

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        plane: str
            coordinate plane to plot (options: 'xy', 'yz', 'xz')

        xr: list of float
            two element list specifying x-axis range

        yr: list of float
            two element list specifying y-axis range

        coord: str
            coordinate system

    """
    spacecraft_colors = [(0,0,0), (213/255,94/255,0), (0,158/255,115/255), (86/255,180/255,233/255)]

    mec_vars = mms_load_mec(trange=trange, data_rate=data_rate, probe=probes, varformat='*_r_' + coord, time_clip=True)

    if len(mec_vars) == 0:
        print('Problem loading MEC data')
        return

    plane = plane.lower()
    coord = coord.lower()

    if plane not in ['xy', 'yz', 'xz']:
        print('Error, invalid plane specified; valid options are: xy, yz, xz')
        return

    if coord not in ['eci', 'gsm', 'geo', 'sm', 'gse', 'gse2000']:
        print('Error, invalid coordinate system specified; valid options are: eci, gsm, geo, sm, gse, gse2000')
        return

    km_in_re = 6371.2

    fig, axis = plt.subplots(sharey=True, sharex=True)

    im = plt.imread(os.path.dirname(os.path.realpath(__file__)) + '/mec/earth_polar1.png')
    plt.imshow(im, extent=(-1, 1, -1, 1))
    plot_count = 0

    for probe in probes:
        position_data = get_data('mms' + str(probe) + '_mec_r_' + coord)
        if position_data is None:
            print('No ' + data_rate + ' MEC data found for ' + 'MMS' + str(probe))
            continue
        else:
            t, d = position_data
            plot_count += 1

        if plane == 'xy':
            axis.plot(d[:, 0]/km_in_re, d[:, 1]/km_in_re, label='MMS' + str(probe), color=spacecraft_colors[int(probe)-1])
            axis.set_xlabel('X Position, Re')
            axis.set_ylabel('Y Position, Re')
        if plane == 'yz':
            axis.plot(d[:, 1]/km_in_re, d[:, 2]/km_in_re, label='MMS' + str(probe), color=spacecraft_colors[int(probe)-1])
            axis.set_xlabel('Y Position, Re')
            axis.set_ylabel('Z Position, Re')
        if plane == 'xz':
            axis.plot(d[:, 0]/km_in_re, d[:, 2]/km_in_re, label='MMS' + str(probe), color=spacecraft_colors[int(probe)-1])
            axis.set_xlabel('X Position, Re')
            axis.set_ylabel('Z Position, Re')

        axis.set_aspect('equal')

    if plot_count > 0: # at least one plot created
        axis.legend()
        axis.set_title(trange[0] + ' to ' + trange[1])
        axis.annotate(coord.upper() + ' coordinates', xy=(0.6, 0.05), xycoords='axes fraction')
        if xr is not None:
            axis.set_xlim(xr)
        if yr is not None:
            axis.set_ylim(yr)

        plt.show()

