"""
This function has now been deprecated. Please use pytplot.tplot_math.tdpwrspc instead.

"""
import logging
from pytplot import tdpwrspc as pytplot_tdpwrspc


def tdpwrspc(
    varname,
    newname=None,
    trange=["0.0", "0.0"],
    nboxpoints=None,
    nshiftpoints=None,
    polar=False,
    bin=3,
    nohanning=False,
    noline=False,
    notperhz=False,
    notmvariance=False,
):
    logging.warning(
        "This function has now been deprecated. Please use pytplot.tplot_math.tdpwrspc instead."
    )

    return pytplot_tdpwrspc(
        varname,
        newname=newname,
        trange=trange,
        nboxpoints=nboxpoints,
        nshiftpoints=nshiftpoints,
        polar=polar,
        bin=bin,
        nohanning=nohanning,
        noline=noline,
        notperhz=notperhz,
        notmvariance=notmvariance,
    )
