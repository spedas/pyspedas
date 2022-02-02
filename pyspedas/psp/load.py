from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2018-11-5', '2018-11-6'], 
         instrument='fields', 
         datatype='mag_rtn', 
         spec_types=None, # for DFB AC spectral data
         level='l2',
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads Parker Solar Probe data into tplot variables; this function is not 
    meant to be called directly; instead, see the wrappers: 
        psp.fields: FIELDS data
        psp.spc: Solar Probe Cup data
        psp.spe: SWEAP/SPAN-e data
        psp.spi: SWEAP/SPAN-i data
        psp.epihi: ISoIS/EPI-Hi data
        psp.epilo: ISoIS/EPI-Lo data
        psp.epi ISoIS/EPI (merged Hi-Lo) data
    
    """

    # remote path formats are going to be all lowercase
    datatype = datatype.lower()

    file_resolution = 24*3600.

    if instrument == 'fields':
        # 4_per_cycle and 1min are daily, not 6h like the full resolution 'mag_(rtn|sc)'
        if datatype == 'mag_rtn_1min' or datatype == 'mag_sc_1min':
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v??.cdf'
        elif datatype == 'mag_rtn_4_per_cycle' or datatype == 'mag_rtn_4_sa_per_cyc':
            pathformat = instrument + '/' + level + '/mag_rtn_4_per_cycle/%Y/psp_fld_' + level + '_mag_rtn_4_sa_per_cyc_%Y%m%d_v??.cdf'
        elif datatype == 'mag_sc_4_per_cycle' or datatype == 'mag_sc_4_sa_per_cyc':
            pathformat = instrument + '/' + level + '/mag_sc_4_per_cycle/%Y/psp_fld_' + level + '_mag_sc_4_sa_per_cyc_%Y%m%d_v??.cdf'
        elif datatype == 'rfs_hfr' or datatype == 'rfs_lfr' or datatype == 'rfs_burst' or datatype == 'f2_100bps':
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v??.cdf'
        elif datatype == 'dfb_dc_spec' or datatype == 'dfb_ac_spec' or datatype == 'dfb_dc_xspec' or datatype == 'dfb_ac_xspec':
            out_vars = []
            for item in spec_types:
                loaded_data = load(trange=trange, instrument=instrument, datatype=datatype + '_' + item, level=level, 
                    suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
                    downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)
                if loaded_data != []:
                    out_vars.extend(loaded_data)
            return out_vars
        elif datatype[:12] == 'dfb_dc_spec_' or datatype[:12] == 'dfb_ac_spec_' or datatype[:13] == 'dfb_dc_xspec_' or datatype[:13] == 'dfb_ac_xspec_':
            if datatype[:13] == 'dfb_dc_xspec_' or datatype[:13] == 'dfb_ac_xspec_':
                dtype_tmp = datatype[:12]
                stype_tmp = datatype[13:]
            else:
                dtype_tmp = datatype[:11]
                stype_tmp = datatype[12:]
            pathformat = instrument + '/' + level + '/' + dtype_tmp + '/' + stype_tmp + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v??.cdf'

        else:
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d%H_v??.cdf'
            file_resolution = 6*3600.
    elif instrument == 'spc':
        pathformat = 'sweap/spc/' + level + '/' + datatype + '/%Y/psp_swp_spc_' + datatype + '_%Y%m%d_v??.cdf'
    elif instrument == 'spe':
        pathformat = 'sweap/spe/' + level + '/' + datatype + '/%Y/psp_swp_sp?_*_%Y%m%d_v??.cdf'
    elif instrument == 'spi':
        pathformat = 'sweap/spi/' + level + '/' + datatype + '/%Y/psp_swp_spi_*_%Y%m%d_v??.cdf'
    elif instrument == 'epihi':
        pathformat = 'isois/epihi/' + level + '/' + datatype + '/%Y/psp_isois-epihi_' + level + '*_%Y%m%d_v??.cdf'
    elif instrument == 'epilo':
        pathformat = 'isois/epilo/' + level + '/' + datatype + '/%Y/psp_isois-epilo_' + level + '*_%Y%m%d_v??.cdf'
    elif instrument == 'epi':
        pathformat = 'isois/merged/' + level + '/' + datatype + '/%Y/psp_isois_' + level + '-' + datatype + '_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange, res=file_resolution)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
