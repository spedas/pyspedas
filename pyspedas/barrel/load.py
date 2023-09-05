from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=None, 
         probe='1A',
         datatype='sspc', 
         level='l2',
         version='v10',
         get_support_data=False,
         files='',
         notplot=False,
         downloadonly=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the BARREL mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.barrel.sspc
        pyspedas.barrel.mspc
        pyspedas.barrel.fspc
        pyspedas.barrel.magn
        pyspedas.barrel.ephm
        pyspedas.barrel.rcnt
        pyspedas.barrel.hkpg

    """
    if not isinstance(probe, list):
        probe = [probe]
    
    if trange is None:
        trange = CONFIG['defaults'][probe[0]]

    out_files = []
    for prb in probe:
        remote_path = (
            str(level) + '/' + str(prb) + '/' + str(datatype) +
            '/bar_' + str(prb) + '_' + str(level) + '_' + str(datatype) + '_%Y%m%d_' + str(version) + '.cdf'
        )

        remote_names = [name.lower() for name in dailynames(file_format=remote_path, trange=trange)]

        files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'],
                         local_path=CONFIG['local_data_dir'], no_download=no_update)
        if files is not None:
            for file in files:
                out_files.append(file)

    out_files = sorted(out_files)
    
    if downloadonly:
        return out_files

    #Convert the cdf files to tvars.
    # Make sure each of the variables is prefixed with the flight ID
    tvars=[]
    for file in out_files:
        p_start = file.find("bar_")
        p_end = file.find("_", p_start + len("bar_"))
        flight = str.upper(file[p_start+len("bar_"):p_end + 1])
        prefix = "brl"+flight
        tvars = tvars + cdf_to_tplot(out_files, prefix=prefix, get_support_data=get_support_data, notplot=notplot)

    if tvars is None:
        return

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
