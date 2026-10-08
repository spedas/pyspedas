from urllib.parse import urlparse

import cdflib

from pyspedas.tplot_tools import time_clip as tclip
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.tplot_tools import cdf_to_tplot

from pyspedas.projects.erg.config import CONFIG

def _spdf_path(pathformat):
    """Translate an ERG-SC satellite template to SPDF's product layout."""
    pathformat = pathformat.replace('/%Y/%m/', '/%Y/')
    parts = pathformat.split('/')
    filename = parts[-1]
    tokens = filename.split('_')
    if parts[0] == 'orb' and parts[1] != 'l3':
        parts.insert(1, 'l2')
    elif parts[0] == 'mgf' and parts[2] != '8sec':
        parts[2] += '_' + tokens[4]
    elif parts[:2] == ['pwe', 'efd']:
        if parts[3] in ['E64Hz', 'E256Hz']:
            parts[3] += '_' + tokens[5]
        parts[3] = parts[3].lower()
        for product in ['E64Hz', 'E256Hz', 'E_spin', 'pot8Hz']:
            parts[-1] = parts[-1].replace(product, product.lower())
    elif parts[:2] == ['pwe', 'hfa']:
        if parts[2] == 'l2':
            parts[3:5] = [parts[3] + '_' + parts[4]]
        else:
            parts.insert(3, '1min')
    elif parts[:2] == ['pwe', 'wfc']:
        component = 'elect' if tokens[4] == 'e' else 'mag'
        datatype = 'wave' if tokens[5] == 'waveform' else 'spec'
        mode = tokens[6]
        if datatype == 'wave':
            mode += '_' + tokens[7]
        parts[3:4] = [component, datatype, mode]
    elif parts[0] == 'mepi' and parts[2] == 'tof':
        parts[2] = tokens[3]
    return '/'.join(parts)


def load(trange=['2017-03-27', '2017-03-28'],
         pathformat=None,
         instrument='mgf',
         datatype='8sec',
         mode=None,
         site=None,
         model=None,
         level='l2',
         prefix='',
         suffix='',
         file_res=24*3600.,
         get_support_data=False,
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         uname=None,
         passwd=None,
         time_clip=False,
         version=None,
         force_download=False):
    """
    This function is not meant to be called directly; please see the instrument specific wrappers:
        pyspedas.projects.erg.mgf()
        pyspedas.projects.erg.hep()
        pyspedas.projects.erg.orb()
        pyspedas.projects.erg.lepe()
        pyspedas.projects.erg.lepi()
        pyspedas.projects.erg.mepe()
        pyspedas.projects.erg.mepi()
        pyspedas.projects.erg.pwe_ofa()
        pyspedas.projects.erg.pwe_efd()
        pyspedas.projects.erg.pwe_hfa()
        pyspedas.projects.erg.xep()
    """

    # File paths are relative to the selected data-family URL for both remote
    # access and the local cache.
    if pathformat.startswith('satellite/erg/'):
        path_prefix = 'satellite/erg/'
        remote_path = CONFIG['satellite_remote_data_dir']
    elif pathformat.startswith('ground/'):
        path_prefix = 'ground/'
        remote_path = CONFIG['ground_remote_data_dir']
    else:
        path_prefix = ''
        remote_path = CONFIG['remote_data_dir']
    remote_format = pathformat[len(path_prefix):]
    last_version = any(char in pathformat for char in '?*')

    if path_prefix == 'satellite/erg/' and urlparse(remote_path).hostname == 'spdf.gsfc.nasa.gov':
        remote_format = _spdf_path(remote_format)

    remote_names = dailynames(file_format=remote_format, trange=trange, res=file_res)
    files = download(remote_file=remote_names,
                     remote_path=remote_path.rstrip('/') + '/',
                     local_path=CONFIG['local_data_dir'],
                     no_download=no_update or CONFIG["no_download"],
                     last_version=last_version, username=uname, password=passwd,
                     force_download=force_download)
    out_files = sorted(set(files or []))

    if downloadonly:
        return out_files

    new_cdflib = False
    if cdflib.__version__ > "0.4.9":
        new_cdflib = True
    else:
        new_cdflib = False

    tvars = cdf_to_tplot(out_files, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                         varformat=varformat, varnames=varnames, notplot=notplot)

    if notplot:
        if len(out_files) > 0:
            cdf_file = cdflib.CDF(out_files[-1])
            cdf_info = cdf_file.cdf_info()
            if new_cdflib:
                all_cdf_variables = cdf_info.rVariables + cdf_info.zVariables
            else:
                all_cdf_variables = cdf_info["rVariables"] + cdf_info["zVariables"]
            gatt = cdf_file.globalattsget()
            for var in all_cdf_variables:
                t_plot_name = prefix + var + suffix
                if t_plot_name in tvars:
                    vatt = cdf_file.varattsget(var)
                    tvars[t_plot_name]['CDF'] = {'VATT':vatt,
                                                'GATT':gatt,
                                                'FILENAME':out_files}
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
