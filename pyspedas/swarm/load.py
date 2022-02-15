from pyspedas import time_string, time_double
from pyspedas.analysis.time_clip import time_clip as tclip
from pyspedas.hapi.hapi import hapi
from .config import CONFIG

def load(trange=['2017-03-27/06:00', '2017-03-27/08:00'], 
         probe='a',
         instrument='vfm',
         datatype='', 
         level='l1b', 
         suffix='', 
         varnames=[], # should be sent to hapi as parameters?
         time_clip=False):
    """
    This function loads data from the Swarm mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.swarm.vfm

    """

    if not isinstance(probe, list):
        probe = [probe]

    tr = time_string(time_double(trange), fmt='%Y-%m-%dT%H:%M:%S')

    for this_probe in probe:
        if instrument == 'vfm':
            tvars = hapi(trange=tr, server=CONFIG['remote_data_dir'] + 'hapi/', dataset='SW_OPER_MAG' + this_probe.upper() + '_' + datatype.upper() + '_' + level[1:].upper(), parameters=varnames)

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
