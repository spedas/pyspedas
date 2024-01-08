"""
This function has now been deprecated. Please use pytplot.tplot_math.dpwrspc instead.

"""
import logging
from pytplot import dpwrspc as pytplot_dpwrspc


def dpwrspc(
    time,
    quantity,
    nboxpoints=256,
    nshiftpoints=128,
    bin=3,
    tbegin=-1.0,
    tend=-1.0,
    noline=False,
    nohanning=False,
    notperhz=False,
    notmvariance=False,
    tm_sensitivity=None,
):
    logging.warning(
        "This function has now been deprecated. Please use pytplot.tplot_math.dpwrspc instead."
    )

    return pytplot_dpwrspc(
        time,
        quantity,
        nboxpoints=nboxpoints,
        nshiftpoints=nshiftpoints,
        bin=bin,
        tbegin=tbegin,
        tend=tend,
        noline=noline,
        nohanning=nohanning,
        notperhz=notperhz,
        notmvariance=notmvariance,
        tm_sensitivity=tm_sensitivity,
    )
