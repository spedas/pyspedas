
from .dpwrspc import dpwrspc
from pytplot import get_data, store_data, options, split_vec

def tdpwrspc(varname, newname=None, nboxpoints=256, nshiftpoints=128, binsize=3, nohanning=False, noline=False, notperhz=False, notmvariance=False):
    if newname is None:
        newname = varname + '_dpwrspc'

    data_tuple = get_data(varname)

    if data_tuple is not None:
        if data_tuple[1][0].shape != ():
            split_vars = split_vec(varname)
            out_vars = []
            for var in split_vars:
                out_vars.append(tdpwrspc(var, newname=var + '_dpwrspc', nboxpoints=nboxpoints, nshiftpoints=nshiftpoints))
            return out_vars
        else:
            pwrspc = dpwrspc(data_tuple[0], data_tuple[1], nboxpoints=nboxpoints, nshiftpoints=nshiftpoints, binsize=binsize, nohanning=nohanning, noline=noline, notperhz=notperhz, notmvariance=notmvariance)

            if pwrspc != None:
                store_data(newname, data={'x': pwrspc[0], 'y': pwrspc[2], 'v': pwrspc[1]})
                options(newname, 'spec', True)
                options(newname, 'ylog', True)
                options(newname, 'zlog', True)
                options(newname, 'Colormap', 'jet')
               # options(newname, 'yrange', [0.01, 16])
        return newname
