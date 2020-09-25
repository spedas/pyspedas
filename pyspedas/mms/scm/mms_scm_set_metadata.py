from pytplot import options

def mms_scm_set_metadata(tnames, probe, datatype, coord, suffix=''):
    """
    This function updates the metadata for the SCM data products
    
    Parameters:
        tnames : list of str
            list of tplot variables loaded by the load routine

        probe : str 
            spacecraft probe #, valid values for MMS probes are ['1', '2', '3', '4']. 

        datatype : str 
            SCM datatype loaded

        coord : str or list of str
            SCM coordinate system; depends on data level
            
        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """

    if not isinstance(tnames, list): tnames = [tnames]

    for tvar in tnames:
        if tvar == 'mms'+probe+'_scm_'+datatype+'_'+coord+suffix:
            options(tvar, 'color', ['b', 'g', 'r'])
            options(tvar, 'ytitle', 'MMS'+probe+' '+datatype+' ('+coord+')')
            options(tvar, 'legend_names', ['1', '2', '3'])
        elif tvar == 'mms'+probe+'_scm_acb_'+coord+'_scsrvy_srvy_l2'+suffix:
            options(tvar, 'color', ['b', 'g', 'r'])
            options(tvar, 'legend_names', ['Bx', 'By', 'Bz'])
            options(tvar, 'ytitle', 'MMS'+probe+' SCM '+datatype+' [nT]')
        elif tvar == 'mms'+probe+'_scm_acb_'+coord+'_scb_brst_l2'+suffix:
            options(tvar, 'color', ['b', 'g', 'r'])
            options(tvar, 'legend_names', ['Bx', 'By', 'Bz'])
            options(tvar, 'ytitle', 'MMS'+probe+' SCM '+datatype+' [nT]')
        elif tvar == 'mms'+probe+'_scm_acb_'+coord+'_schb_brst_l2'+suffix:
            options(tvar, 'color', ['b', 'g', 'r'])
            options(tvar, 'legend_names', ['Bx', 'By', 'Bz'])
            options(tvar, 'ytitle', 'MMS'+probe+' SCM '+datatype+' [nT]')
