import cdflib

from pyspedas.analysis.time_clip import time_clip as tclip
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import cdf_to_tplot

from .config import CONFIG

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
         version=None):
    """
    This function is not meant to be called directly; please see the instrument specific wrappers:
        pyspedas.erg.mgf()
        pyspedas.erg.hep()
        pyspedas.erg.orb()
        pyspedas.erg.lepe()
        pyspedas.erg.lepi()
        pyspedas.erg.mepe()
        pyspedas.erg.mepi()
        pyspedas.erg.pwe_ofa()
        pyspedas.erg.pwe_efd()
        pyspedas.erg.pwe_hfa()
        pyspedas.erg.xep()
    """

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat,
                              trange=trange, res=file_res)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG[
                     'local_data_dir'], no_download=no_update, last_version=True, username=uname, password=passwd)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                         varformat=varformat, varnames=varnames, notplot=notplot)

    if notplot:
        if len(out_files) > 0:
            cdf_file = cdflib.CDF(out_files[-1])
            cdf_info = cdf_file.cdf_info()
            all_cdf_variables = cdf_info['rVariables'] + cdf_info['zVariables']
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
