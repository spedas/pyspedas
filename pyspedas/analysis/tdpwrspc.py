"""
Compute power spectra for a tplot variable.

Calls dpwrspc for the actual computation.

Notes
-----
Similar to tdpwrspc.pro in IDL SPEDAS.

"""
from .dpwrspc import dpwrspc
from pytplot import get_data, store_data, options, split_vec


def tdpwrspc(varname, newname=None, nboxpoints=256, nshiftpoints=128,
             binsize=3, nohanning=False, noline=False, notperhz=False,
             notmvariance=False):
    """
    Compute power spectra for a tplot variable.

    Parameters
    ----------
    varname: str
        Name of pytplot variable.
    newname: str, optional
        Name of new pytplot variable to save data to.
    nboxpoints: int, optional
        The number of points to use for the hanning window.
        The default is 256.
    nshiftpoints: int, optional
        The number of points to shift for each spectrum.
        The default is 128.
    binsize: int, optional
        Size for binning of the data along the frequency domain.
        The default is 3.
    nohanning: bool, optional
        If True, no hanning window is applied to the input.
        The default is False.
    noline: bool, optional
        If True, no straight line is subtracted.
        The default is False.
    notperhz: bool, optional
        If True, the output units are the square of the input units.
        The default is False.
    notmvariance: bool, optional
        If True, replace output spectrum for any windows that have variable.
        cadence with NaNs.
        The default is False.

    Returns
    -------
    str
        Name of new pytplot variable.

    """
    if newname is None:
        newname = varname + '_dpwrspc'

    data_tuple = get_data(varname)

    if data_tuple is not None:
        if data_tuple[1][0].shape != ():
            split_vars = split_vec(varname)
            out_vars = []
            for var in split_vars:
                out_vars.append(tdpwrspc(var, newname=var + '_dpwrspc',
                                         nboxpoints=nboxpoints,
                                         nshiftpoints=nshiftpoints,
                                         binsize=binsize,
                                         nohanning=nohanning,
                                         noline=noline, notperhz=notperhz,
                                         notmvariance=notmvariance))
            return out_vars
        else:
            pwrspc = dpwrspc(data_tuple[0], data_tuple[1],
                             nboxpoints=nboxpoints,
                             nshiftpoints=nshiftpoints,
                             binsize=binsize,
                             nohanning=nohanning,
                             noline=noline, notperhz=notperhz,
                             notmvariance=notmvariance)

            if pwrspc is not None:
                store_data(newname, data={'x': pwrspc[0],
                                          'y': pwrspc[2],
                                          'v': pwrspc[1]})
                options(newname, 'spec', True)
                options(newname, 'ylog', True)
                options(newname, 'zlog', True)
                options(newname, 'Colormap', 'jet')
                # options(newname, 'yrange', [0.01, 16])
        return newname
