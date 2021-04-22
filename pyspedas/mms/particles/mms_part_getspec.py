
import pyspedas
from pyspedas.mms.particles.mms_part_products import mms_part_products

def mms_part_getspec(instrument='fpi', probe='1', species='e', data_rate='fast', 
    trange=None, output=['energy', 'theta', 'phi'], units='eflux'):
    """

    """
    
    fpi_vars = pyspedas.mms.fpi(datatype='d'+species+'s-dist', probe=probe, data_rate=data_rate, trange=trange, time_clip=True)

    if not isinstance(probe, list):
        probe = [probe]

    out_vars = []

    for prb in probe:

        if instrument == 'fpi':
            tname = 'mms'+str(prb)+'_d'+species+'s_dist_'+data_rate

        new_vars = mms_part_products(tname, species=species, instrument=instrument, probe=probe, data_rate=data_rate,
                          units=units)
        out_vars = out_vars + new_vars

    return out_vars