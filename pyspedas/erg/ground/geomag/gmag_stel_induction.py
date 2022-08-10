
from .gmag_isee_induction import gmag_isee_induction

def gmag_stel_induction(
    trange=['2018-10-18/00:00:00','2018-10-18/02:00:00'],
    suffix='',
    site='all',
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    uname=None,
    passwd=None,
    time_clip=False,
    ror=True,
    frequency_dependent=False
):

    return gmag_isee_induction(
                                trange=trange,
                                suffix=suffix,
                                site=site,
                                get_support_data=get_support_data,
                                varformat=varformat,
                                varnames=varnames,
                                downloadonly=downloadonly,
                                notplot=notplot,
                                no_update=no_update,
                                uname=uname,
                                passwd=passwd,
                                time_clip=time_clip,
                                ror=ror,
                                frequency_dependent=frequency_dependent
                                )
