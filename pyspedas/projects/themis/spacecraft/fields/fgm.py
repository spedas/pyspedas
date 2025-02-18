
from pyspedas.projects.themis.load import load
from pytplot import options

def fgm(trange=['2007-03-23', '2007-03-24'],
        probe='c',
        level='l2',
        suffix='',
        get_support_data=False,
        varformat=None,
        coord=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads Fluxgate magnetometer (FGM) data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2007-03-23', '2007-03-24']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')
            Default: 'c'

        level: str
            Data level; Valid options: 'l1', 'l2'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  
            Default: False; only loads data with a "VAR_TYPE" attribute of "data"

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None; all variables are loaded

        varnames: list of str
            List of variable names to load
            Default: Empty list, so all data variables are loaded

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified
            in the trange keyword
            Default: False

    Returns
    -------
    List of str
        List of tplot variables created
        Empty list if no data
    
    Example
    -------
        >>> import pyspedas
        >>> from pyspedas import tplot
        >>> fgm_vars = pyspedas.projects.themis.fgm(probe='d', trange=['2013-11-5', '2013-11-6'])
        >>> tplot(['thd_fgs_btotal', 'thd_fgs_gse'])

    """

    varformat = check_args(varformat=varformat, level=level, coord=coord)

    loaded_vars = load(instrument='fgm', trange=trange, level=level,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames,
                downloadonly=downloadonly, notplot=notplot,
                probe=probe, time_clip=time_clip, no_update=no_update)

    if loaded_vars is None or loaded_vars == []:
        return []

    if not isinstance(level, list):
        level = [level]

    if not isinstance(probe, list):
        probe = [probe]

    fgm_types = ['fgs', 'fgl', 'fgh', 'fge']
    possible_coords = ['gse', 'gsm', 'dsl', 'ssl']

    # set some plot metadata
    for prb in probe:
        for lvl in level:
            if lvl == 'l2':
                for fgm_type in fgm_types:
                    for coord_sys in possible_coords:
                        if 'th'+prb+'_'+fgm_type+'_'+coord_sys+suffix in loaded_vars:
                            options('th'+prb+'_'+fgm_type+'_'+coord_sys+suffix, 'ytitle', 'TH'+prb.upper()+' '+fgm_type.upper())
                            options('th'+prb+'_'+fgm_type+'_'+coord_sys+suffix, 'color', ['b', 'g', 'r'])
                            options('th'+prb+'_'+fgm_type+'_'+coord_sys+suffix, 'legend_names', ['Bx '+coord_sys.upper(), 'By '+coord_sys.upper(), 'Bz '+coord_sys.upper()])
                    if 'th'+prb+'_'+fgm_type+'_btotal'+suffix in loaded_vars:
                        options('th'+prb+'_'+fgm_type+'_btotal'+suffix, 'ytitle', 'TH'+prb.upper()+' '+fgm_type.upper())
                        options('th'+prb+'_'+fgm_type+'_btotal'+suffix, 'legend_names', 'Bmag')

    return loaded_vars


def check_args(varformat=None, level='l2', coord=None):
    """
    Return varformat for fgm data

    Parameters:
        varformat: str, optional
            If is not empty return as is
        level: {'l1', 'l2'}, optional
            Data level
        coord: {'ssl', 'dsl', 'gse', 'gsm'}, optional
             Coordinate system. If set to None all possible values are used. coord is applicable for level='l2'

    Returns: str
        varformat for themis.load
    """

    # DEV COMMENTS:
    # If varformat is set to None then assign default value
    # We construct regular expression that covers the fgm variable format
    # IDL thm_load_xxx function has the following input:
    #   vsnames = 'a b c d e', $
    #   type_sname = 'probe', $
    #   vdatatypes = 'fgl fgh fge', $
    #   vlevels = 'l1 l2', $ - This input is inherited
    #   vL2datatypes = 'fgs fgl fgh fge fgs_btotal fgl_btotal fgh_btotal fge_btotal', $
    #   vL2coord = 'ssl dsl gse gsm none', $
    # Resulted "varformat" for 'l2' and default coodr ('dsl') is:
    #  th?_fgs_dsl th?_fgl_dsl th?_fgh_dsl th?_fge_dsl
    #  th?_fgs_btotal_dsl th?_fgl_btotal_dsl th?_fgh_btotal_dsl th?_fge_btotal_dsl
    #  th?_fgs th?_fgl th?_fgh th?_fge
    #  th?_fgs_btotal th?_fgl_btotal th?_fgh_btotal th?_fge_btotal
    # Resulted "varformat" for 'l1' is:
    #  *fgl* *fgh* *fge*

    import re

    if varformat is None:
        if level == 'l2':
            # Prepare coordinates, we reuse the same regex to check the coord variable
            coord_regexp = '(ssl|dsl|gse|gsm){1}'
            coord_str = coord_regexp

            # If coord is set and it matches the pattern, then include it into varformat
            if coord is not None and re.search(coord_regexp, coord, re.IGNORECASE):
                coord_str = '(' + coord.lower() + '){1}'

            varformat = '^th[a-e]{1}_(fgs|fgl|fgh|fge){1}(_btotal)?(_{1}' + coord_str + ')?$'
        else:  # This case must be 'l1'
            varformat = '^th[a-e]{1}_(fgl|fgh|fge){1}*'  # keep right end open with '*' (wildcard)

    return varformat
