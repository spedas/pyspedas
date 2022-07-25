"""
@Author: Xin Cao, Xiangning Chu, University of Colorado Boulder
The vector and contour map plots are implemented for initial investigation.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import TwoSlopeNorm, Normalize, SymLogNorm, NoNorm, LogNorm #, CenteredNorm
from .config import CONFIG
from itertools import chain
from matplotlib.path import Path
from pyspedas.secs import read_data_files
from datetime import datetime, timedelta
from pyspedas.utilities.dailynames import dailynames
from mpl_toolkits.basemap.solar import daynight_terminator
import logging
#os.environ['PROJ_LIB'] = '/Users/cao/anaconda3/envs/secs/share/proj'
#if an error about "dedent" occurs, downgrade the matplotlib version to 3.2.0 by using "pip install -U matplotlib==3.2"
try:
    from mpl_toolkits.basemap import Basemap
except ImportError:
    logging.info('Error importing Basemap; installation instructions can be found at: https://matplotlib.org/basemap/users/installing.html or https://anaconda.org/anaconda/basemap')


class CenteredNorm(Normalize):
    """
    This function is directly contributed from the latest matplotlib version,
    but not included in the 3.2.0 version, so is duplicated here.
    """
    def __init__(self, vcenter=0, halfrange=None, clip=False):
        """
        Normalize symmetrical data around a center (0 by default).
        Unlike `TwoSlopeNorm`, `CenteredNorm` applies an equal rate of change
        around the center.
        Useful when mapping symmetrical data around a conceptual center
        e.g., data that range from -2 to 4, with 0 as the midpoint, and
        with equal rates of change around that midpoint.
        Parameters
        ----------
        vcenter : float, default: 0
            The data value that defines ``0.5`` in the normalization.
        halfrange : float, optional
            The range of data values that defines a range of ``0.5`` in the
            normalization, so that *vcenter* - *halfrange* is ``0.0`` and
            *vcenter* + *halfrange* is ``1.0`` in the normalization.
            Defaults to the largest absolute difference to *vcenter* for
            the values in the dataset.
        Examples
        --------
        This maps data values -2 to 0.25, 0 to 0.5, and 4 to 1.0
        (assuming equal rates of change above and below 0.0):
            >>> import matplotlib.colors as mcolors
            >>> norm = mcolors.CenteredNorm(halfrange=4.0)
            >>> data = [-2., 0., 4.]
            >>> norm(data)
            array([0.25, 0.5 , 1.  ])
        """
        super().__init__(vmin=None, vmax=None, clip=clip)
        self._vcenter = vcenter
        # calling the halfrange setter to set vmin and vmax
        self.halfrange = halfrange

    def _set_vmin_vmax(self):
        """
        Set *vmin* and *vmax* based on *vcenter* and *halfrange*.
        """
        self.vmax = self._vcenter + self._halfrange
        self.vmin = self._vcenter - self._halfrange

    def autoscale(self, A):
        """
        Set *halfrange* to ``max(abs(A-vcenter))``, then set *vmin* and *vmax*.
        """
        A = np.asanyarray(A)
        self._halfrange = max(self._vcenter-A.min(),
                              A.max()-self._vcenter)
        self._set_vmin_vmax()

    def autoscale_None(self, A):
        """Set *vmin* and *vmax*."""
        A = np.asanyarray(A)
        if self._halfrange is None and A.size:
            self.autoscale(A)

    @property
    def vcenter(self):
        return self._vcenter

    @vcenter.setter
    def vcenter(self, vcenter):
        if vcenter != self._vcenter:
            self._vcenter = vcenter
            self._changed()
        if self.vmax is not None:
            # recompute halfrange assuming vmin and vmax represent
            # min and max of data
            self._halfrange = max(self._vcenter-self.vmin,
                                  self.vmax-self._vcenter)
            self._set_vmin_vmax()

    @property
    def halfrange(self):
        return self._halfrange

    @halfrange.setter
    def halfrange(self, halfrange):
        if halfrange is None:
            self._halfrange = None
            self.vmin = None
            self.vmax = None
        else:
            self._halfrange = abs(halfrange)

    def __call__(self, value, clip=None):
        if self._halfrange is not None:
            # enforce symmetry, reset vmin and vmax
            self._set_vmin_vmax()
        return super().__call__(value, clip=clip)


def draw_map(m, scale=0.2):
    """
    This function is for data visualization with geographic map.
    Parameter m: basemap object
    """
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)

    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)

    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')
    return


def noon_midnight_meridian(dtime=None, delta=0.25):
    """
    This function calculates the longtitude and latitude of the noon-midnight meridian
    based on a given UTC time.
    :param dtime: the str of UTC time, which is of the format of 'year-month-day/hour:minute:second'
    :param delta: float or int, in degree, which is the interval of neighbor points on the meridian.
    :return: dictionary with keys: 'lons_noonmidnight', 'lats_noonmidnight', 'lons_noon', 'lats_noon'
                                    'lons_midnight', 'lats_midnight'
                        with values of numpy arrays
    """
    # method2:
    n_interval = 360 / delta + 1
    ni_half = int(np.floor(n_interval / 2))
    ni_otherhalf = int(n_interval - ni_half)

    time_current_UTC = datetime.strptime(dtime, '%Y-%m-%d/%H:%M:%S')
    dtime_noon = dtime[0:11] + '12:00:00'
    # print('dtime_noon: ', dtime_noon)
    time_noon = datetime.strptime(dtime_noon, '%Y-%m-%d/%H:%M:%S')
    time_diff = time_noon - time_current_UTC
    diff_in_hours = time_diff.total_seconds() / 3600  # within [-12,12] hours due to the same day.
    if diff_in_hours == 0:
        lons_latmax = 0  # current UTC time is just at noon
        lons_latmin = 180  # midnight longitude
    elif diff_in_hours > 0:
        lons_latmax = 0 + 15 * diff_in_hours  # longitude for noon line
        lons_latmin = lons_latmax - 180  # longitude for midnight line
    elif diff_in_hours < 0:
        lons_latmax = 0 - 15 * diff_in_hours  # longitude for noon line
        lons_latmin = lons_latmax + 180  # longitude for midnight line
    #
    lons_max_arr = np.full((1, ni_half), lons_latmax)  # for noon line
    lats_max_arr = np.linspace(-90, 90, ni_half)  # for noon line

    lons_min_arr = np.full((1, ni_otherhalf), lons_latmin)  # for midnight line
    lats_min_arr = np.linspace(90, -90, ni_otherhalf)  # for midnight line

    lons_arr = np.concatenate((lons_max_arr, lons_min_arr), axis=None)
    lats_arr = np.concatenate((lats_max_arr, lats_min_arr), axis=None)
    lons_nm, lats_nm = lons_arr, lats_arr  # the whole noon-midnight circle

    lons_n, lats_n = lons_max_arr[0], lats_max_arr  # the noon semi-circle
    lons_m, lats_m = lons_min_arr[0], lats_min_arr  # the midnight semi-circle

    noon_midnight = {'lons_noonmidnight': lons_nm, 'lats_noonmidnight': lats_nm,
                     'lons_noon': lons_n, 'lats_noon': lats_n,
                     'lons_midnight': lons_m, 'lats_midnight': lats_m}
    return noon_midnight


def _make_EICS_plots(dtime=None, vplot_sized=False, contour_den=8, s_loc=False, quiver_scale=30, pred = False, pred_var = None, plot_title_addon = None, colormaplimit=None, EICS_component='Jy'):
    """
    @Parameter: dtime input as a string
    @Parameter: s_loc input as a bool, which means the locations of the virtual stations.
    """
    dtype = 'EICS'

    if not os.path.exists(CONFIG['plots_dir']):
        os.makedirs(CONFIG['plots_dir'])
    dtime_range = [dtime, dtime]
    pathformat_prefix = dtype + '/%Y/%m/'
    pathformat_unzipped = pathformat_prefix + '%d/' + dtype + '%Y%m%d_%H%M%S.dat'
    filename_unzipped = dailynames(file_format=pathformat_unzipped, trange=dtime_range, res=10)
    out_files_unzipped = [CONFIG['local_data_dir'] + rf_res for rf_res in filename_unzipped]
    Data_Days_time = read_data_files(out_files=out_files_unzipped, dtype=dtype, out_type='df')

    if pred == True: # XC
        obs_var = Data_Days_time['Jy']
        print(np.size(pred_var), np.size(Data_Days_time['Jy']), np.shape(pred_var), np.shape(Data_Days_time['Jy']))
        if np.size(pred_var) != np.size(Data_Days_time['Jy']):
            raise ValueError('np.size(pred_var) != np.size(Data_Days_time[Jy]) !')
        #if np.shape(pred_var) != np.shape(Data_Days_time['Jy']):
        #    raise ValueError('np.shape(pred_var) != np.shape(Data_Days_time[Jy]) !')
        pred_var = np.reshape(pred_var, np.shape(Data_Days_time['Jy']))
        if np.shape(pred_var) == np.shape(Data_Days_time['Jy']):
            print(' pred_var has the same size and shape with Data_Days_time[Jy] !')
        Data_Days_time['Jy'] = pred_var

    J_comp = Data_Days_time['Jy']
    Jc_max, Jc_min = J_comp.max(), J_comp.min()
    Jcm_abs = max(abs(Jc_max), abs(Jc_min))
    contour_density = np.linspace(-Jcm_abs, Jcm_abs, num=contour_den)
    tp = dtime
    datetime_tp = tp[0:4] + tp[5:7] + tp[8:10] + '_' + tp[11:13] + tp[14:16] + tp[17:19]
    lon = Data_Days_time['longitude']
    lat = Data_Days_time['latitude']
    Jx = Data_Days_time['Jx']  # Note: positive is Northward
    Jy = Data_Days_time['Jy']  # Note: positive is Eastward

    # plot 1:
    # plot map ground (North hemisphere)
    fig1 = plt.figure(figsize=(8, 8))
    ax1 = plt.gca()

    m = Basemap(projection='lcc', resolution='c',
                width=8E6, height=8E6,
                lat_0=60, lon_0=-100)
    # draw coastlines, country boundaries, fill continents.
    m.drawcoastlines(linewidth=0.25)
    m.drawcountries(linewidth=0.25)
    m.fillcontinents(color='None', lake_color='None')
    # draw the edge of the map projection region (the projection limb)
    m.drawmapboundary(fill_color=None)
    # m.drawgreatcircle(-100,0,0,90)
    m.drawlsmask()
    # m.bluemarble()
    m.shadedrelief()
    # draw parallels and meridians.
    # label parallels on right and top
    # meridians on bottom and left
    parallels = np.arange(0., 81, 10.)
    # labels = [left,right,top,bottom]
    m.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(10., 351., 20.)
    m.drawmeridians(meridians, labels=[True, False, False, True])
    date_nightshade = datetime.strptime(dtime, '%Y-%m-%d/%H:%M:%S')
    m.nightshade(date=date_nightshade)
    draw_map(m)

    # plot vector field:
    print('lon before: ', lon)
    lon = lon.to_numpy()
    lat = lat.to_numpy()
    print('lon after:  ', lon)
    Jx = Jx.to_numpy()  # Note: positive is Northward
    Jy = Jy.to_numpy()  # Note: positive is Eastward
    Jx_uni = Jx / np.sqrt(Jx ** 2 + Jy ** 2)
    Jy_uni = Jy / np.sqrt(Jx ** 2 + Jy ** 2)
    n = -2
    color = np.sqrt(((Jx_uni - n) / 2) ** 2 + ((Jy_uni - n) / 2) ** 2)
    if vplot_sized == False:
        qv = m.quiver(lon, lat, Jx_uni, Jy_uni, color, headlength=7, latlon=True,
                      cmap='GnBu')  # autumn_r #, color=cm(norm(o)))#, cmap = 'jet')
        plt.colorbar()
    else:
        Jy_rot, Jx_rot, x, y = m.rotate_vector(Jy, Jx, lon, lat, returnxy=True)
        qv = m.quiver(lon, lat, Jy_rot, Jx_rot, headlength=7, latlon=True, scale_units='dots',
                      scale=quiver_scale)  # , transform='lcc')

        qk = ax1.quiverkey(qv, 0.3, -0.1, 100, r'$100 \ mA/m$', labelpos='E', coordinates='data')  # figure


    plt.title(label='EICS ' + tp, fontsize=20, color="black", pad=20)
    plt.tight_layout()
    plt.savefig(CONFIG['plots_dir'] + 'EICS' + '_vector_' + date_nightshade.strftime('%Y%m%d%H%M%S') + '.jpeg')
    plt.show()

    # plot 2: contour plot
    # plot map ground (North hemisphere)
    fig2 = plt.figure(figsize=(8, 8))
    ax2 = plt.gca()
    m = Basemap(projection='lcc', resolution='c',
                width=8E6, height=8E6,
                lat_0=60, lon_0=-100)
    # draw coastlines, country boundaries, fill continents.
    m.drawcoastlines(linewidth=0.25)
    m.drawcountries(linewidth=0.25)
    m.fillcontinents(color='None', lake_color='None')
    # draw the edge of the map projection region (the projection limb)
    m.drawmapboundary(fill_color=None)
    m.drawlsmask()
    m.shadedrelief()
    # draw parallels and meridians.
    # label parallels on right and top
    # meridians on bottom and left
    parallels = np.arange(0., 81, 10.)
    m.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(10., 351., 20.)
    m.drawmeridians(meridians, labels=[True, False, False, True])

    date_nightshade = datetime.strptime(dtime, '%Y-%m-%d/%H:%M:%S')
    # m.nightshade(date=date_nightshade, alpha = 0.0)

    delta = 0.25
    lons_dd, lats_dd, tau, dec = daynight_terminator(date_nightshade, delta, m.lonmin, m.lonmax)
    xy = [lons_dd, lats_dd]
    xy = np.array(xy)
    xb, yb = xy[0], xy[1]
    m.plot(xb, yb, marker=None, color='m', latlon=True)  # for dawn-dusk circle line

    # Plot the noon-midnight line.
    n_interval = len(lons_dd)
    ni_half = int(np.floor(len(lons_dd) / 2))
    ni_otherhalf = n_interval - ni_half


    noon_midnight = noon_midnight_meridian(dtime, delta)

    m.plot(noon_midnight['lons_noon'], noon_midnight['lats_noon'], marker=None, color='deepskyblue',
           latlon=True)  # noon semi-circle

    m.plot(noon_midnight['lons_midnight'], noon_midnight['lats_midnight'], marker=None, color='k',
           latlon=True)  # midnight semi-circle

    draw_map(m)

    Jy_log = Jy / np.abs(Jy) * np.log10(np.abs(Jy))
    Jy_log = Jy / np.abs(Jy) * np.log10(np.abs(Jy)) ##
    if colormaplimit == None:
        norm_cb = CenteredNorm()
    else:
        norm_cb = CenteredNorm(halfrange=colormaplimit)
    # norm_cb = NoNorm()
    # norm_cb = CenteredNorm(vmin=Jy.min(), vcenter=0, vmax=Jy.max())
    # use Jy for the contour map, not Jy_rot.
    if EICS_component == 'Jy':
        ctrf = m.contourf(lon, lat, Jy, contour_density, latlon=True, tri=True, cmap='jet_r', norm=norm_cb)
    elif EICS_component == 'Jx':
        ctrf = m.contourf(lon, lat, Jx, contour_density, latlon=True, tri=True, cmap='jet_r', norm=norm_cb)
    ##ctrf = m.contourf(lon, lat, Jy, contour_density, latlon=True, tri=True, cmap='jet_r', norm=norm_cb)
    # -------------
    if s_loc:
        m.scatter(lon, lat, latlon=True, marker='*', c='black')
    FAC_loc = False
    if FAC_loc: # for 2008-02-29 and 2008-02-22 events' field aligned current locations:
        import pandas as pd
        event_df_a = pd.read_csv('/Users/xica3495/Downloads/event_locs/scwsnapshot_step1_nosubSQ_V2.txt', delimiter="\s+")
        event_df_b = pd.read_csv('/Users/xica3495/Downloads/event_locs/scwsnapshot_step2_nosubSQ_V2.txt', delimiter="\s+")
        event_df_c = pd.read_csv('/Users/xica3495/Downloads/event_locs/scwsnapshot_step3_nosubSQ_V2.txt', delimiter="\s+")
        event_df_d = pd.read_csv('/Users/xica3495/Downloads/event_locs/scwsnapshot_step4_nosubSQ_V2.txt', delimiter="\s+")
        #print('cp00!')
        #print(dtime)
        #print(event_df.loc[0,'time'])
        #print(dtime==event_df.loc[0,'time'])
        row_event_df_a = event_df_a[event_df_a['time'] == dtime]
        row_event_df_b = event_df_b[event_df_b['time'] == dtime]
        row_event_df_c = event_df_c[event_df_c['time'] == dtime]
        row_event_df_d = event_df_d[event_df_d['time'] == dtime]
        #print(row_event_df)
        #print(row_event_df['lat1_geo'].to_numpy()[0], type(row_event_df['lat1_geo'].to_numpy()[0]))
        lon1_ev_a = row_event_df_a['lon1_geo'].to_numpy()[0]
        lon2_ev_a = row_event_df_a['lon2_geo'].to_numpy()[0]
        lat1_ev_a = row_event_df_a['lat1_geo'].to_numpy()[0]
        lat2_ev_a = row_event_df_a['lat2_geo'].to_numpy()[0]

        lon1_ev_b = row_event_df_b['lon1_geo'].to_numpy()[0]
        lon2_ev_b = row_event_df_b['lon2_geo'].to_numpy()[0]
        lat1_ev_b = row_event_df_b['lat1_geo'].to_numpy()[0]
        lat2_ev_b = row_event_df_b['lat2_geo'].to_numpy()[0]

        lon1_ev_c = row_event_df_c['lon1_geo'].to_numpy()[0]
        lon2_ev_c = row_event_df_c['lon2_geo'].to_numpy()[0]
        lat1_ev_c = row_event_df_c['lat1_geo'].to_numpy()[0]
        lat2_ev_c = row_event_df_c['lat2_geo'].to_numpy()[0]

        lon1_ev_d = row_event_df_d['lon1_geo'].to_numpy()[0]
        lon2_ev_d = row_event_df_d['lon2_geo'].to_numpy()[0]
        lat1_ev_d = row_event_df_d['lat1_geo'].to_numpy()[0]
        lat2_ev_d = row_event_df_d['lat2_geo'].to_numpy()[0]


        m.scatter(lon1_ev_a, lat1_ev_a, latlon=True, marker='o', s=20, c='red')
        m.scatter(lon2_ev_a, lat2_ev_a, latlon=True, marker='o', s=20, c='blue')

        m.scatter(lon1_ev_b, lat1_ev_b, latlon=True, marker='*', s=20, c='red')
        m.scatter(lon2_ev_b, lat2_ev_b, latlon=True, marker='*', s=20, c='blue')

        m.scatter(lon1_ev_c, lat1_ev_c, latlon=True, marker='^', s=20, c='red')
        m.scatter(lon2_ev_c, lat2_ev_c, latlon=True, marker='^', s=20, c='blue')

        m.scatter(lon1_ev_d, lat1_ev_d, latlon=True, marker='D', s=20, c='red')
        m.scatter(lon2_ev_d, lat2_ev_d, latlon=True, marker='D', s=20, c='blue')

        #print(event_df.loc[0,:])
        #print(event_df.loc[1,:])
        #print(event_df.loc[2,['lat1_geo', 'lat2_geo']])
        #print(event_df['lon2_sm'])
        print('cp01!')
    # -------------
    cb = m.colorbar(matplotlib.cm.ScalarMappable(norm=norm_cb, cmap='jet_r'), pad='15%')
    if EICS_component == 'Jy':
        cb.set_label(r'$\mathit{J}_y \  (mA/m)$')
    elif EICS_component == 'Jx':
        cb.set_label(r'$\mathit{J}_x \  (mA/m)$')
    ax_cb = cb.ax
    text = ax_cb.yaxis.label
    font_cb = matplotlib.font_manager.FontProperties(family='times new roman', style='italic', size=20)
    text.set_font_properties(font_cb)
    if pred == True:
        if plot_title_addon != None:
            plt.title(label= plot_title_addon + ' Predicted EICS ' + tp, fontsize=20, color="black", pad=20)
        else:
            plt.title(label= 'Predicted EICS ' + tp, fontsize=20, color="black", pad=20)
    else:
        plt.title(label='EICS ' + tp, fontsize=20, color="black", pad=20)
    plt.tight_layout()
    if pred == True:
        if EICS_component == 'Jy':
            plt.savefig(CONFIG['plots_dir'] + 'EICS_Jy' + '_pred' + '_contour_' + date_nightshade.strftime('%Y%m%d%H%M%S') + '.jpeg')
        elif EICS_component == 'Jx':
            plt.savefig(CONFIG['plots_dir'] + 'EICS_Jx' + '_pred' + '_contour_' + date_nightshade.strftime(
                '%Y%m%d%H%M%S') + '.jpeg')
    else:
        if EICS_component == 'Jy':
            plt.savefig(CONFIG['plots_dir'] + 'EICS_Jy' + '_contour_' + date_nightshade.strftime('%Y%m%d%H%M%S') + '.jpeg')
        elif EICS_component == 'Jx':
            plt.savefig(CONFIG['plots_dir'] + 'EICS_Jx' + '_contour_' + date_nightshade.strftime('%Y%m%d%H%M%S') + '.jpeg')

    plt.show()

    # plot the visual grids:

    fig3 = plt.figure(figsize=(8, 8))
    ax3 = plt.gca()
    m = Basemap(projection='lcc', resolution='c',
                width=8E6, height=8E6,
                lat_0=60, lon_0=-100)
    # draw coastlines, country boundaries, fill continents.
    m.drawcoastlines(linewidth=0.25)
    m.drawcountries(linewidth=0.25)
    m.fillcontinents(color='None', lake_color='None')
    # draw the edge of the map projection region (the projection limb)
    m.drawmapboundary(fill_color=None)
    m.drawlsmask()
    m.shadedrelief()
    # draw parallels and meridians.
    # label parallels on right and top
    # meridians on bottom and left
    parallels = np.arange(0., 81, 10.)
    m.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(10., 351., 20.)
    m.drawmeridians(meridians, labels=[True, False, False, True])

    date_nightshade = datetime.strptime(dtime, '%Y-%m-%d/%H:%M:%S')
    # m.nightshade(date=date_nightshade, alpha = 0.0)

    delta = 0.25
    lons_dd, lats_dd, tau, dec = daynight_terminator(date_nightshade, delta, m.lonmin, m.lonmax)
    xy = [lons_dd, lats_dd]
    xy = np.array(xy)
    xb, yb = xy[0], xy[1]
    m.plot(xb, yb, marker=None, color='m', latlon=True)  # for dawn-dusk circle line

    # Plot the noon-midnight line.
    n_interval = len(lons_dd)
    ni_half = int(np.floor(len(lons_dd) / 2))
    ni_otherhalf = n_interval - ni_half

    noon_midnight = noon_midnight_meridian(dtime, delta)

    m.plot(noon_midnight['lons_noon'], noon_midnight['lats_noon'], marker=None, color='deepskyblue',
           latlon=True)  # noon semi-circle

    m.plot(noon_midnight['lons_midnight'], noon_midnight['lats_midnight'], marker=None, color='k',
           latlon=True)  # midnight semi-circle

    draw_map(m)

    # -------------
    VG_labels = np.linspace(0, len(lon)-1, len(lon), dtype=int)
    m.scatter(lon, lat, latlon=True, marker='*', c='black')

    x_shift, y_shift = (-5, 5)
    for i, vg_label in enumerate(VG_labels):
        lon_tmp, lat_tmp = m(lon[i], lat[i])
        plt.annotate(str(vg_label), xy=(lon_tmp, lat_tmp), xycoords='data', xytext=(x_shift, y_shift), textcoords='offset points', color='r', fontsize=6) #xy=(lon[i], lat[i])
    # -------------
    font_cb = matplotlib.font_manager.FontProperties(family='times new roman', style='italic', size=20)
    text.set_font_properties(font_cb)
    plt.title(label='EICS visual grids' + tp, fontsize=20, color="black", pad=20)
    plt.tight_layout()
    plt.savefig(CONFIG['plots_dir'] + 'EICS' + '_VisualGrids_' + date_nightshade.strftime('%Y%m%d%H%M%S') + '.pdf')
    plt.show()



    print('EICS plots completed!')
    return


def _make_SECS_plots(data=None, dtime=None, contour_den=8, s_loc=False):
    """
    @Parameter: dtime input as a string
    @Parameter: s_loc input as a bool, which means the locations of the virtual stations.
    """
    dtype = 'SECS'

    if not os.path.exists(CONFIG['plots_dir']):
        os.makedirs(CONFIG['plots_dir'])
    dtime_range = [dtime, dtime]
    pathformat_prefix = dtype + '/%Y/%m/'
    pathformat_unzipped = pathformat_prefix + '%d/' + dtype + '%Y%m%d_%H%M%S.dat'
    filename_unzipped = dailynames(file_format=pathformat_unzipped, trange=dtime_range, res=10)
    out_files_unzipped = [CONFIG['local_data_dir'] + rf_res for rf_res in filename_unzipped]
    Data_Days_time = read_data_files(out_files=out_files_unzipped, dtype=dtype, out_type='df')

    J_comp = Data_Days_time['J']
    Jc_max, Jc_min = J_comp.max(), J_comp.min()
    Jcm_abs = max(abs(Jc_max), abs(Jc_min))
    contour_density = np.linspace(-Jcm_abs, Jcm_abs, num=contour_den)
    tp = dtime
    datetime_tp = tp[0:4] + tp[5:7] + tp[8:10] + '_' + tp[11:13] + tp[14:16] + tp[17:19]
    lon = Data_Days_time['longitude']
    lat = Data_Days_time['latitude']
    J = Data_Days_time['J']

    lon = lon.to_numpy()
    lat = lat.to_numpy()
    J = J.to_numpy()

    # plot 1: contour plot
    # plot map ground (North hemisphere)
    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution='c',
                width=8E6, height=8E6,
                lat_0=60, lon_0=-100)
    # draw coastlines, country boundaries, fill continents.
    m.drawcoastlines(linewidth=0.25)
    m.drawcountries(linewidth=0.25)
    m.fillcontinents(color='None', lake_color='None')
    # draw the edge of the map projection region (the projection limb)
    m.drawmapboundary(fill_color=None)
    m.drawlsmask()
    m.shadedrelief()
    # draw parallels and meridians.
    # label parallels on right and top
    # meridians on bottom and left
    parallels = np.arange(0., 81, 10.)
    m.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(10., 351., 20.)
    m.drawmeridians(meridians, labels=[True, False, False, True])

    date_nightshade = datetime.strptime(dtime, '%Y-%m-%d/%H:%M:%S')
    delta = 0.25
    lons_dd, lats_dd, tau, dec = daynight_terminator(date_nightshade, delta, m.lonmin, m.lonmax)
    xy = [lons_dd, lats_dd]
    xy = np.array(xy)
    xb, yb = xy[0], xy[1]
    m.plot(xb, yb, marker=None, color='b', latlon=True)

    # Plot the noon-midnight line.
    n_interval = len(lons_dd)
    ni_half = int(np.floor(len(lons_dd) / 2))
    ni_otherhalf = n_interval - ni_half

    noon_midnight = noon_midnight_meridian(dtime, delta)

    m.plot(noon_midnight['lons_noon'], noon_midnight['lats_noon'], marker=None, color='deepskyblue',
           latlon=True)  # noon semi-circle

    m.plot(noon_midnight['lons_midnight'], noon_midnight['lats_midnight'], marker=None, color='k',
           latlon=True)  # midnight semi-circle

    draw_map(m)

    norm_cb = CenteredNorm()
    ctrf = m.contourf(lon, lat, J, contour_density, latlon=True, tri=True, cmap=plt.get_cmap('seismic', 20),
                      norm=norm_cb)
    if s_loc:
        m.scatter(lon, lat, latlon=True, marker='*', c='black')
    cb = m.colorbar(matplotlib.cm.ScalarMappable(norm=norm_cb, cmap='seismic'), pad='15%')
    cb.set_label(r'$\mathit{J} \  (A)$')
    ax_cb = cb.ax
    text = ax_cb.yaxis.label
    font_cb = matplotlib.font_manager.FontProperties(family='times new roman', style='italic', size=20)
    text.set_font_properties(font_cb)
    plt.title(label='SECS ' + tp, fontsize=20, color="black", pad=20)
    plt.tight_layout()
    plt.savefig(CONFIG['plots_dir'] + 'SECS' + '_' + date_nightshade.strftime('%Y%m%d%H%M%S') + '.jpeg')
    plt.show()
    print('SECS plots completed!')
    return


def make_plots(dtype='EICS', dtime=None, vplot_sized=True, contour_den=100, s_loc=False, quiver_scale=30, pred = False, pred_var = None, plot_title_addon = None, colormaplimit=None, EICS_component='Jy'):  # or SECS
    """
        This wrapper function to plot the vector and contour map for SECS/EICS data

        Parameters
        ----------
            dtime: str
                Set the single time point of interest with the format
                'YYYY-MM-DD/hh:mm:ss'

            dtype: str
                Data type; valid options: 'EICS' or 'SECS'

            vplot_sized: bool
                Set this flag to plot the EICS' vector field for Jx, Jy with the length for the J's magnitude.

            contour_den: int
                Set the density of the contour map.

            s_loc: bool
                Set this flag to superimpose the virtual stations on the contour map.

        Returns
        ----------
            None.
        """
    if dtype == 'EICS':
        _make_EICS_plots(dtime=dtime, vplot_sized=vplot_sized, contour_den=contour_den, s_loc=s_loc, quiver_scale=quiver_scale, pred = pred, pred_var = pred_var, plot_title_addon = plot_title_addon, colormaplimit=colormaplimit, EICS_component=EICS_component)
        # make a vector map and a contour map.
    if dtype == 'SECS':
        _make_SECS_plots(dtime=dtime, contour_den=contour_den, s_loc=s_loc)
        # make a contour map.
    return
