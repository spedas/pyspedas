from .gmag_isee_fluxgate import gmag_isee_fluxgate

def gmag_stel_fluxgate(
    trange=['2020-08-01', '2020-08-02'],
    suffix='',
    site='all',
    datatype='all',
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    uname=None,
    passwd=None,
    time_clip=False,
    ror=True
):
    
    return gmag_isee_fluxgate(trange=trange,
                              suffix=suffix,
                              site=site,
                              datatype=datatype,
                              get_support_data=get_support_data,
                              varformat=varformat,
                              varnames=varnames,
                              downloadonly=downloadonly,
                              notplot=notplot,
                              no_update=no_update,
                              uname=uname,
                              passwd=passwd,
                              time_clip=time_clip,
                              ror=ror)