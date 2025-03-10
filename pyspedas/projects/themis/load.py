import logging
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['2013-11-5', '2013-11-6'],
         instrument='fgm',
         probe='c',
         level='l2',
         datatype=None, # ASK data, ESD (3d L2 ESA)
         stations=None,  # ground mag and ASK data
         greenland=None,  # also for ground mag data
         prefix='',
         suffix='',
         get_support_data=False,
         varformat=None,
         exclude_format=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False,
         force_download=False,
         ):
    """
    This function loads data from the THEMIS mission;
    this function is not meant to be called directly;
    instead, see the wrappers:
        pyspedas.projects.themis.fgm
        pyspedas.projects.themis.fit
        pyspedas.projects.themis.efi
        pyspedas.projects.themis.scm
        pyspedas.projects.themis.fft
        pyspedas.projects.themis.fbk
        pyspedas.projects.themis.esa
        pyspedas.projects.themis.esd
        pyspedas.projects.themis.sst
        pyspedas.projects.themis.mom
        pyspedas.projects.themis.gmom
        pyspedas.projects.themis.gmag
        pyspedas.projects.themis.ask
        pyspedas.projects.themis.state
        pyspedas.projects.themis.slp

    """

    if not isinstance(probe, list):
        probe = [probe]

    out_files = []
    file_resolution = 24*3600.0 # default to daily files
    varformat_tmp = None #used for ASK data, when site is input, so that possible varformat input is not overwritten


    for prb in probe:

        # Remote data directory (CDAWeb for SSC data)
        remote_data_dir = CONFIG['remote_data_dir']

        if instrument == 'ask':
            if stations is None:
                pathformat = ('thg/' + level + '/asi/ask/%Y/thg_' + level + '_ask'
                              + '_%Y%m%d_v01.cdf')
            else:
#This code block loads ASF data, not ask
#                # individual station data should have hourly files
#                file_resolution = 3600.0
#                pathformat = ('thg/' + level + '/asi/' + stations + '/%Y/%m/'
#                              + 'thg_' + level + '_' + datatype + '_' + stations
#                              + '_%Y%m%d%H_v01.cdf')
                pathformat = ('thg/' + level + '/asi/ask/%Y/thg_' + level + '_ask'
                              + '_%Y%m%d_v01.cdf')
                #Usurp varformat input to get the appropriate site variable
                varformat_tmp = '*'+stations+'*'
        elif instrument == 'fgm':
            pathformat = ('th' + prb + '/' + level + '/' + instrument
                          + '/%Y/th' + prb + '_' + level + '_' + instrument
                          + '_%Y%m%d_v??.cdf')
        elif instrument == 'fit':
            pathformat = ('th' + prb + '/' + level + '/' + instrument
                          + '/%Y/th' + prb + '_' + level + '_' + instrument
                          + '_%Y%m%d_v??.cdf')
        elif instrument == 'efi':
            if level == 'l2':
                pathformat = ('th' + prb + '/' + level + '/' + instrument
                              + '/%Y/th' + prb + '_' + level + '_' + instrument
                              + '_%Y%m%d_v??.cdf')
            elif level == 'l1':
                pathformat = [('th' + prb + '/' + level + '/vaf/%Y/th' + prb
                               + '_' + level + '_vaf_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/vap/%Y/th' + prb
                               + '_' + level + '_vap_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/vaw/%Y/th' + prb
                               + '_' + level + '_vaw_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/vbf/%Y/th' + prb
                               + '_' + level + '_vbf_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/vbp/%Y/th' + prb
                               + '_' + level + '_vbp_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/vbw/%Y/th' + prb
                               + '_' + level + '_vbw_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/eff/%Y/th' + prb
                              + '_' + level + '_eff_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/efw/%Y/th' + prb
                               + '_' + level + '_efw_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/efp/%Y/th' + prb
                               + '_' + level + '_efp_%Y%m%d_v??.cdf')]
        elif instrument == 'scm':
            if level == 'l2':
                pathformat = ('th' + prb + '/' + level + '/' + instrument
                              + '/%Y/th' + prb + '_' + level + '_' + instrument
                              + '_%Y%m%d_v??.cdf')
            elif level == 'l1':
                pathformat = [('th' + prb + '/' + level + '/scp/%Y/th' + prb
                               + '_' + level + '_scp_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/scf/%Y/th' + prb
                               + '_' + level + '_scf_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/scw/%Y/th' + prb
                               + '_' + level + '_scw_%Y%m%d_v??.cdf')]
        elif instrument == 'fft':
            if level == 'l2':
                pathformat = ('th' + prb + '/' + level + '/' + instrument
                              + '/%Y/th' + prb + '_' + level + '_' + instrument
                              + '_%Y%m%d_v??.cdf')
            elif level == 'l1':
                pathformat = [('th' + prb + '/' + level + '/fff_16/%Y/th' + prb
                               + '_' + level + '_fff_16_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/fff_32/%Y/th' + prb
                               + '_' + level + '_fff_32_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/fff_64/%Y/th' + prb
                               + '_' + level + '_fff_64_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/ffp_16/%Y/th' + prb
                               + '_' + level + '_ffp_16_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/ffp_32/%Y/th' + prb
                               + '_' + level + '_ffp_32_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/ffp_64/%Y/th' + prb
                               + '_' + level + '_ffp_64_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/ffw_16/%Y/th' + prb
                               + '_' + level + '_ffw_16_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/ffw_32/%Y/th' + prb
                               + '_' + level + '_ffw_32_%Y%m%d_v??.cdf'),
                              ('th' + prb + '/' + level + '/ffw_64/%Y/th' + prb
                               + '_' + level + '_ffw_64_%Y%m%d_v??.cdf')]
        elif instrument == 'fbk':
            pathformat = ('th' + prb + '/' + level + '/' + instrument
                          + '/%Y/th' + prb + '_' + level + '_' + instrument
                          + '_%Y%m%d_v??.cdf')
        elif instrument == 'esa':
            pathformat = ('th' + prb + '/' + level + '/' + instrument
                          + '/%Y/th' + prb + '_' + level + '_' + instrument
                          + '_%Y%m%d_v??.cdf')
        elif instrument == 'esd':
            level = 'l2' #For all ESD data
            pathformat = ('th' + prb + '/' + level + '/' + instrument
                          + '/%Y/th' + prb + '_' + level + '_esa_' + datatype
                          + '_%Y%m%d_v??.cdf')
        elif instrument == 'sst':
            pathformat = ('th' + prb + '/' + level + '/' + instrument
                          + '/%Y/th' + prb + '_' + level + '_' + instrument
                          + '_%Y%m%d_v??.cdf')
        elif instrument == 'mom':
            pathformat = ('th' + prb + '/' + level + '/' + instrument
                          + '/%Y/th' + prb + '_' + level + '_' + instrument
                          + '_%Y%m%d_v??.cdf')
        elif instrument == 'gmom':
            pathformat = ('th' + prb + '/' + level + '/' + instrument
                          + '/%Y/th' + prb + '_' + level + '_' + instrument
                          + '_%Y%m%d_v??.cdf')
        elif instrument == 'state':
            if 'spdf' in remote_data_dir:
                # There is no unversioned link at SPDF, specify a versioned file with wildcard.
                pathformat = ('th' + prb + '/' + level + '/' + instrument
                              + '/%Y/th' + prb + '_' + level + '_' + instrument
                              + '_%Y%m%d_v??.cdf')
            else:
                # Load the unversioned file, which should be a link to the highest version
                pathformat = ('th' + prb + '/' + level + '/' + instrument
                              + '/%Y/th' + prb + '_' + level + '_' + instrument
                              + '_%Y%m%d.cdf')
        elif instrument == 'slp':
            # note: v01 hard-coded in IDL version as well
            pathformat = 'slp/' + level + '/eph/%Y/slp_l1_eph_%Y%m%d_v01.cdf'
        elif instrument == 'ssc':
            # current/past orbit data from CDAWeb
            pathformat = 'th' + prb + '/ssc/%Y/th' + prb + '_or_ssc' + '_%Y%m01_v??.cdf'
            remote_data_dir = 'https://cdaweb.gsfc.nasa.gov/pub/data/themis/'
        elif instrument == 'ssc_pre':
            # predicted orbit data from CDAWeb
            pathformat = 'th' + prb + '/ssc_pre/%Y/th' + prb + 'pred_or_ssc' + '_%Y0101_v??.cdf'
            remote_data_dir = 'https://cdaweb.gsfc.nasa.gov/pub/data/themis/'
        elif instrument == 'gmag':
            if stations is None:
                logging.error('No stations specified')
                return
            else:
                pathformat = []
                for site, in_greenland in zip(stations, greenland):
                    if site == 'idx':
                        # THEMIS GMAG index files are only L1
                        pathformat.append('thg/l1/mag/idx/%Y/thg_l1_idx_%Y%m%d_v??.cdf')
                    elif in_greenland:
                        pathformat.append('thg/greenland_gmag/' + level
                                          + '/' + site + '/%Y/thg_' + level
                                          + '_mag_' + site + '_%Y%m%d_v??.cdf')
                    else:
                        pathformat.append('thg/' + level + '/mag/' + site
                                          + '/%Y/thg_' + level + '_mag_' + site
                                          + '_%Y%m%d_v??.cdf')

        if not isinstance(pathformat, list):
            pathformat = [pathformat]

        for file_format in pathformat:
            # find the full remote path names using the trange
            remote_names = dailynames(file_format=file_format, trange=trange, res=file_resolution)

            files = download(remote_file=remote_names,
                             remote_path=remote_data_dir,
                             local_path=CONFIG['local_data_dir'],
                             no_download=no_update,
                             last_version=True,
                             force_download=force_download,)
            if files is not None:
                for file in files:
                    out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    if varformat_tmp is None:
        tvars = cdf_to_tplot(out_files,
                             prefix=prefix,
                             suffix=suffix,
                             get_support_data=get_support_data,
                             varformat=varformat,
                             exclude_format=exclude_format,
                             varnames=varnames,
                             notplot=notplot)
    else:
        tvars = cdf_to_tplot(out_files,
                             prefix=prefix,
                             suffix=suffix,
                             get_support_data=get_support_data,
                             varformat=varformat_tmp,
                             exclude_format=exclude_format,
                             varnames=varnames,
                             notplot=notplot)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
