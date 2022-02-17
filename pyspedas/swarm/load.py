from pyspedas import time_string, time_double
from pyspedas.analysis.time_clip import time_clip as tclip
from pyspedas.hapi.hapi import hapi
from .config import CONFIG

def load(trange=['2017-03-27/06:00', '2017-03-27/08:00'], 
         probe='a',
         instrument='mag',
         datatype='', 
         level='l1b', 
         suffix='', 
         varnames=[], # should be sent to hapi as parameters?
         time_clip=False):
    """
    This function loads data from the Swarm mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.swarm.mag

    """
    server = CONFIG['remote_data_dir'] + 'hapi/'

    if not isinstance(probe, list):
        probe = [probe]

    tr = time_string(time_double(trange), fmt='%Y-%m-%dT%H:%M:%S')

    out_vars = []

    for this_probe in probe:
        prefix = 'swarm' + this_probe.lower() + '_'
        if instrument == 'mag':
            dataset = 'SW_OPER_MAG' + this_probe.upper() + '_' + datatype.upper() + '_' + level[1:].upper()
            tvars = hapi(trange=tr, 
                         server=server, 
                         dataset=dataset, 
                         parameters=varnames, 
                         suffix=suffix, 
                         prefix=prefix)

            if tvars is not None and len(tvars) != 0:
                out_vars.extend(tvars)

    if time_clip:
        for new_var in out_vars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return out_vars
