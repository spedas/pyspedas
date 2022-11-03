from .load import load
import numpy as np
import pandas as pd
from pytplot import store_data, options
from pyspedas import time_double
from pyspedas.cotrans.xyz_to_polar import xyz_to_polar


def pws(trange=['2012-10-01', '2012-10-02'],
        datatype='ne', 
        level='h1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Plasma Waves and Sounder experiment (PWS)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:
                'ne', 'npw-ds', 'npw-py', 'spw'

        level: str
            Data level; options: 'h1' (default: h1)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    tvars = load(instrument='pws', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return pws_postprocessing(tvars)


def pws_postprocessing(variables):
    """
    Placeholder for PWS post-processing 
    """
    return variables


def rdm(trange=['2012-10-01', '2012-10-02'],
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Radiation Moniter (RDM)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    files = load(instrument='rdm', trange=trange, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if files is None or notplot or downloadonly:
        return files

    return rdm_postprocessing(files)


def rdm_postprocessing(files):
    """
    Load the RDM ASCII files into tplot variables
    """
    data = load_csv_file(files)
    values = data.to_numpy()
    unix_times = time_double([ymd + '/' + hms for ymd, hms in zip(values[:, 0], values[:, 1])])

    L = np.float64(values[:, 2])
    INV = np.float64(values[:, 3])
    FMLAT = np.float64(values[:, 4])
    MLAT = np.float64(values[:, 5])
    MLT = np.float64(values[:, 6])
    ALT = np.float64(values[:, 7])
    GLAT = np.float64(values[:, 8])
    GLON = np.float64(values[:, 9])
    RDM_E3 = np.float64(values[:, 10])
    Energy = np.zeros(len(RDM_E3))
    Energy[:] = 2.5

    prefix_project = 'akb_'
    prefix_descriptor = 'rdm_'
    prefix = prefix_project + prefix_descriptor

    store_data(prefix_project+'L', data={'x': unix_times, 'y': L})
    store_data(prefix_project+'INV', data={'x': unix_times, 'y': INV})
    store_data(prefix_project+'FMLAT', data={'x': unix_times, 'y': FMLAT})
    store_data(prefix_project+'MLAT', data={'x': unix_times, 'y': MLAT})
    store_data(prefix_project+'MLT', data={'x': unix_times, 'y': MLT})
    store_data(prefix_project+'ALT', data={'x': unix_times, 'y': ALT})
    store_data(prefix_project+'GLAT', data={'x': unix_times, 'y': GLAT})
    store_data(prefix_project+'GLON', data={'x': unix_times, 'y': GLON})
    store_data(prefix+'FEIO', data={'x': unix_times, 'y': RDM_E3})
    store_data(prefix+'FEIO_Energy', data={'x': unix_times, 'y': Energy})

    options(prefix+'FEIO', 'spec', True)

    options(prefix_project+'L', 'ytitle', 'L-value')
    options(prefix_project+'INV', 'ytitle', 'Invariant Latitude [deg]')
    options(prefix_project+'FMLAT', 'ytitle', 'Footprint Latitude [deg]')
    options(prefix_project+'MLAT', 'ytitle', 'Magnetic Latitude [deg]')
    options(prefix_project+'MLT', 'ytitle', 'Magnetic Local Time [hour]')
    options(prefix_project+'ALT', 'ytitle', 'Altitude [km]')
    options(prefix_project+'GLAT', 'ytitle', 'Geographic Latitude [deg]')
    options(prefix_project+'GLON', 'ytitle', 'Geographic Longitude [deg]')
    options(prefix+'FEIO', 'ytitle', 'Omni-directional Integral Electron Flux')
    options(prefix+'FEIO', 'ysubtitle', '[/cm^22 sec str]')
    options(prefix+'FEIO_Energy', 'ytitle', 'Elctron energy [MeV]')

    return [prefix_project+'L',
            prefix_project+'INV',
            prefix_project+'FMLAT',
            prefix_project+'MLAT',
            prefix_project+'MLT',
            prefix_project+'ALT',
            prefix_project+'GLAT',
            prefix_project+'GLON',
            prefix+'FEIO',
            prefix+'FEIO_Energy']


def orb(trange=['2012-10-01', '2012-10-02'],
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Akebono orbit data (orb)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    files = load(instrument='orb', trange=trange, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if files is None or notplot or downloadonly:
        return files

    return orb_postprocessing(files)


def orb_postprocessing(files):
    """
    Placeholder for orb post-processing 
    """
    prefix_project = 'akb_'
    prefix_descriptor = 'orb_'
    prefix = prefix_project + prefix_descriptor

    cols = ['pass','ut', 'ksc_azm', 'ksc_elv', 'ksc_dis', 'ksc_ang', 'syo_azm', 'syo_elv', 'syo_dis', 'syo_ang',
            'pra_azm', 'pra_elv', 'pra_dis', 'pra_ang', 'esr_azm', 'esr_elv', 'esr_dis', 'esr_ang', 'gclat','gclon',
            'inv', 'fmlat', 'mlat', 'mlt', 'bmdl_x', 'bmdl_y', 'bmdl_z', 'xxlon_sc', 'xxlat_sc', 'aheight','lsun',
            's_direc_x', 's_direc_y', 's_direc_z', 'sc_pos_x', 'sc_pos_y', 'sc_pos_z', 'sc_vel_x', 'sc_vel_y', 'sc_vel_z']

    data = load_csv_file(files, cols=cols)
    values = data.to_numpy()
    unix_times = time_double([date[2:4] + '-' + date[4:6] + '-' + date[0:2] + '/' + date[6:8] + ':' + date[8:10] + ':' + date[10:12] for date in data['ut']])

    km_in_re = 6374.4

    xyz = np.array([[data['sc_pos_x']], [data['sc_pos_y']], [data['sc_pos_z']]]).transpose([2, 0, 1]).squeeze()
    xyz = np.float64(xyz)
    xyz_re = xyz/km_in_re
    r_theta_phi = xyz_to_polar(xyz)
    rr = r_theta_phi[:, 0]
    th = r_theta_phi[:, 1]
    ph = r_theta_phi[:, 2]
    store_data(prefix + 'geo', data={'x': unix_times, 'y': xyz_re})
    store_data(prefix + 'gdlat', data={'x': unix_times, 'y': np.float64(data['gclat'])})
    store_data(prefix + 'gdlon', data={'x': unix_times, 'y': np.float64(data['gclon'])})
    store_data(prefix + 'inv', data={'x': unix_times, 'y': np.float64(data['inv'])})
    store_data(prefix + 'fmlat', data={'x': unix_times, 'y': np.float64(data['fmlat'])})
    store_data(prefix + 'MLT', data={'x': unix_times, 'y': np.float64(data['mlt'])})
    store_data(prefix + 'gcalt', data={'x': unix_times, 'y': rr / km_in_re})
    store_data(prefix + 'gclat', data={'x': unix_times, 'y': th})
    store_data(prefix + 'gclon', data={'x': unix_times, 'y': ph})
    options(prefix + 'geo', 'ytitle', 'GEO')
    options(prefix + 'geo', 'ysubtitle', '[Re]')
    options(prefix + 'gdlat', 'ytitle', 'Geodetic latitude of the magnetic footprint')
    options(prefix + 'gdlat', 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'gdlon', 'ytitle', 'Geodetic longitude of the magnetic footprint')
    options(prefix + 'gdlon', 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'inv', 'ytitle', 'Invariant Latitude of the magnetic footprint')
    options(prefix + 'inv', 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'fmlat', 'ytitle', 'Geomagnetic Latitude of the magnetic footprint')
    options(prefix + 'fmlat', 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'MLT', 'ytitle', 'Magnetic Local Time')
    options(prefix + 'MLT', 'ysubtitle', '[hours]')
    options(prefix + 'gcalt', 'ytitle', 'Geocentric Altitude')
    options(prefix + 'gcalt', 'ysubtitle', '[Re]')
    options(prefix + 'gclat', 'ytitle', 'Geocentric Latitude')
    options(prefix + 'gclat', 'ysubtitle', '[deg]')
    options(prefix + 'gclon', 'ytitle', 'Geocentric Longitude')
    options(prefix + 'gclon', 'ysubtitle', '[deg]')

    return [prefix + 'geo',
            prefix + 'gdlat',
            prefix + 'gdlon',
            prefix + 'inv',
            prefix + 'fmlat',
            prefix + 'MLT',
            prefix + 'gcalt',
            prefix + 'gclat',
            prefix + 'gclon']

        
def load_csv_file(filenames, cols=None):
    """
    function that loads a CSV file into a pandas Data Frame and returns the pandas Data Frame
    the header of the CSV file is:
    PASS       UT           ksc_azm(deg) ksc_elv(deg) ksc_dis(km) ksc_ang(deg) syo_azm(deg) syo_elv(deg) syo_dis(km) syo_ang(deg) pra_azm(deg) pra_elv(deg) pra_dis(km) pra_ang(deg) esr_azm(deg) esr_elv(deg) esr_dis(km) esr_ang(deg) GCLAT(deg) GCLON(deg) INV(deg) FMLAT(deg) MLAT(deg) MLT(h) Bmdl       X       Y       Z (nT) GCLON_S/C(deg) GCLAT_S/C(deg) LSUN ALT(km) s_Direc     s/c_pos     s/c_vel(km/s)
    """
    if not isinstance(filenames, list):
        filenames = [filenames]
    df = pd.concat((pd.read_csv(f, header=0, delim_whitespace=True, dtype=str, names=cols) for f in filenames), ignore_index=True)
    return df
