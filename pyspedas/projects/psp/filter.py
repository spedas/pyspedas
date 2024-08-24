# Filtering Utilities
import enum
import numpy as np
from copy import deepcopy
from collections.abc import Iterable
from pytplot import tplot_names, data_quants, get_timespan, get_data, store_data

def filter_fields(tvars, dqflag = 0, keep = False, names_out = True):
    """
    This function filters on flagged values from PSP FIELDS magnetometer tplot 
    variables based on selected quality flags.  By default it filters OUT the 
    data where selected flags are set, but the keyword parameter "keep" can be 
    set True to keep just the data where the selected quality flags are set.
    
    For each TVAR passed in a new tplot variable is created with the filtered 
    data.  The new name is of the form:  <tvarname>_XXXXXX 
    where each 'XXX' is a 0 padded flag indicator sorted from lowest to highest.
    [If keep=True, the new name is of the form: <tvarname>_KXXXXXX]
 
    Flags 0 and -1 are special cases where the 'keep' flag is ignored

    So, psp.filter_fields('mag_RTN_1min_x',[4,16]) 
        - results in tvar named "mag_RTN_1min_x_004016"
        - tvar holds data where *NEITHER* flag 4 NOR flag 16 is set.

    And, psp.filter_fields('mag_RTN_1min_x',[4,16], keep=True) 
        - results in tvar named "mag_RTN_1min_x_K004016"
        - tvar holds data where *BOTH* flag 4 AND flag 16 is set.

    psp.filter_fields('mag_RTN_1min',0) 
        - results in tvar named "mag_RTN_1min_000"
        - tvar holds data with no set flags
    
    Valid only for variables of type:
        '...psp_fld_l2_mag_...' (full res, 1 minute, or 4 Sa per cycle)
        '...psp_fld_l2_rfs_...' (lfr and hfr) 

    Parameters
    ----------
        tvars: str or list of strings
            Tplot variable names, previously loaded

        dqflag: int or list of ints
            Elements indicate which of the data quality flags
            to filter on.             
            From the set {-1,0,1,2,4,8,16,32,64,128,256,512} 

            For keep=False (default)
            For flags >= 1: filters OUT wherever ANY of the selected flags are set.

            For keep=True
            For flags >= 1: returns data wherever ANY of the selected flags are set.

            Note: if using 0 or -1, no other flags should be selected
            -1: Keep cases with no set flags or only the 128 flag set 
            0: No set flags. (default)
            1: FIELDS antenna bias sweep
            2: PSP thruster firing
            4: SCM Calibration
            8: PSP rotations for MAG calibration (MAG rolls)
            16: FIELDS MAG calibration sequence
            32: SWEAP SPC in electron mode
            64: PSP Solar limb sensor (SLS) test
            128: PSP spacecraft is off umbra pointing  
            256: High frequency noise affecting RFS and TDS receivers. 
            512: Antennas driven towards the FIELDS power supply rails.   

        keep: bool
            If True, for dqflags >=1, return data where any of the selected flags 
            are set.  Otherwise, return data where none of the selected flags 
            are set.  (Default False)

        names_out: bool
            If set, return a list of the tplot variable names created 
            from this filter. Order corresponds to the input array of tvar
            names, so that tvar[i] filtered is in names_out[i]
            (Default True)

    Returns
    ----------
        None or List of tplot variables created if name_out=True (default)
    """

    new_names = [] if names_out else None

    # Check arguments
    if isinstance(tvars, str):
        tvars = [tvars]

    if not isinstance(dqflag, Iterable):
        dqflag = [dqflag]

    for flg in dqflag:
        assert flg in {-1,0,1,2,4,8,16,32,64,128,256,512}, "Bad FIELDS Quality Flag: {}".format(flg)

    if len(dqflag) > 1:
        assert 0 not in dqflag, 'DQFLAG of 0 must be set by itself'
        assert -1 not in dqflag, 'DQFLAG of -1 must be set by itself'

    dqflag.sort()

    # Reduce list to supported variables that are already loaded
    tvars = [x for x in tvars if x in tplot_names(quiet=True)]

    tvars = [x for x in tvars if 'fld_l2_mag_RTN' in x 
                              or 'fld_l2_mag_SC' in x 
                              or 'rfs_lfr' in x
                              or 'rfs_hfr' in x]
    if len(tvars) == 0:
        print("No valid variables for filtering")
        return new_names       

    # Create time specific quality flags as needed
    qf_target = []
    err_flg = []
    keep_var = []
    for tvar in tvars:

        qf_root = data_quants[tvar].qf_root
        if qf_root:
            keep_var.append(tvar)
            if ('rfs_hfr' in tvar) or ('rfs_lfr' in tvar):
                # Lots of possible epoch tags for the rfs data
                tag = '_' + data_quants[tvar].CDF['VATT']['DEPEND_0']
            elif '_1min' in tvar:
                tag = '_1min'
            elif '_4_Sa_per_Cyc' in tvar:
                tag = '_4_per_cycle'
            else:
                tag = '_hires'

            make_qf_var = False
            if qf_root + tag in data_quants.keys():
                # Variable exists.  Is it in the right time range?
                varTR = get_timespan(tvar)
                qfTR = get_timespan(tvar)
                if (qfTR[0] != varTR[0]) or (qfTR[1] != varTR[1]):
                    make_qf_var = True                
            else:
                make_qf_var = True

            if make_qf_var:
                err = _ff_match_qf_epochs(tvar, qf_root, tag)
                err_flg.append(err)
            else:
                err_flg.append(0)

            qf_target.append(qf_root + tag)
        else:
            print("Source quality flags missing. No filtered variabled created for: {}".format(tvar))
    
    # Remove cases where match epochs couldn't work
    valid_tn = [keep_var[i] for i in range(len(keep_var)) if err_flg[i] == 0]
    qf_target = [qf_target[i] for i in range(len(keep_var)) if err_flg[i] == 0]
    bad_tn = [keep_var[i] for i in range(len(keep_var)) if err_flg[i] == 1]
    if len(bad_tn) > 0:
        print("Error creating some matching time quality flags.")
        for tn in bad_tn:
            print("No filtered variabled created for: {}".format(tn))

    # Create the filtered variables
    if len(valid_tn) == 0:
        print("No valid variables for filtering\n")

    else:
        qfmap = dict()
        
        # Handle simpler cases, just the 0 or -1 flag
        if len(dqflag) == 1 and dqflag[0] in [0, -1]:
            # Get the quality flag arrays
            for qfname in qf_target:
                if qfname not in qfmap:
                    d = get_data(qfname)
                    qfmap[qfname] = d.y

            for i, tn in enumerate(valid_tn):
                if dqflag[0] == 0:
                    suffix = '_000'
                    mask = qfmap[qf_target[i]] != 0
                else:
                    suffix = '_0-1'
                    mask = (qfmap[qf_target[i]] != 0) & (qfmap[qf_target[i]] != 128)
                new_attrs = deepcopy(get_data(tn, metadata=True))
                if 'CDF' in new_attrs:
                    _ = new_attrs.pop('CDF')
                new_attrs['qf_root'] = None
                new_attrs['plot_options']['yaxis_opt']['axis_label'] += '\n(flt: {})'.format(suffix)  # TODO: how to increase left margin programmatically so this can be a new line?! (default matplotlib is .1 normal)
                
                data = deepcopy(get_data(tn))
                if issubclass(data.y.dtype.type, np.integer):
                    new_data = {'x':data.times, 'y':data.y.astype(float)}
                else:
                    new_data = {'x':data.times, 'y':data.y}

                try:
                    new_data['v'] = data.v
                except:
                    pass
   
                new_data['y'][mask] = np.nan

                store_data(tn+suffix, new_data, attr_dict=new_attrs)
                if names_out:
                    new_names.append(tn+suffix)

        # Handle multiple flags
        else:
            # Get quality flag arrays and flagged bits
            for qfname in qf_target:
                if qfname not in qfmap:
                    d = get_data(qfname)
                    qfmap[qfname] = dict()
                    qfmap[qfname]['dqf'] = d.y
                    qfmap[qfname]['dqfbits'] = _ff_unpackbits(d.y)

            suffix = '_K' if keep else '_'
            mybits = _ff_unpackbits(np.uint32(0))
            for flg in dqflag:
                suffix += '{:03}'.format(flg)
                mybits += _ff_unpackbits(np.uint32(flg))

            for i, tn in enumerate(valid_tn):
                new_attrs = deepcopy(get_data(tn, metadata=True))
                if 'CDF' in new_attrs:
                    _ = new_attrs.pop('CDF')
                new_attrs['qf_root'] = None
                new_attrs['plot_options']['yaxis_opt']['axis_label'] += '\n(flt: {})'.format(suffix) # TODO: how to increase left margin programmatically so this can be a new line and visisble by default?! (default matplotlib is .1 normal)
                
                data = deepcopy(get_data(tn))
                if issubclass(data.y.dtype.type, np.integer):
                    new_data = {'x':data.times, 'y':data.y.astype(float)}
                else:
                    new_data = {'x':data.times, 'y':data.y}

                try:
                    new_data['v'] = data.v
                except:
                    pass

                rem_mask = np.full(len(new_data['y']), False)
                for j in range(len(mybits)):
                    if mybits[j] == 1:
                        mask = qfmap[qf_target[i]]['dqfbits'][:, j] == 1
                        rem_mask[mask] = True

                if keep:
                    rem_mask = ~rem_mask
                new_data['y'][rem_mask] = np.nan

                if rem_mask.all():
                    #Handle completely empty data case.    
                    print("{}: (Skipped) No data matches this filter".format(tn))
                else:
                    store_data(tn+suffix, new_data, attr_dict=new_attrs)
                    if names_out:
                        new_names.append(tn+suffix)
    return new_names


def _ff_unpackbits(x):
    """
    Like np.unpackbits but works for all uint dtypes (not just uint8)
    Adapated from https://stackoverflow.com/a/51509307
    """
    if np.issubdtype(x.dtype, np.floating):
        raise ValueError("numpy data type needs to be int-like")
    num_bits = 8 * x.dtype.itemsize

    xshape = list(x.shape)
    x = x.reshape([-1, 1])
    mask = 2**np.arange(num_bits, dtype=x.dtype).reshape([1, num_bits])
    return (x & mask).astype(bool).astype(int).reshape(xshape + [num_bits])


def _ff_match_qf_epochs(target, source, tag):
    """
    Helper to psp.filter_fields routine.  Extends the quality_flag variable to
    match the time resolution target.  Results valid only if the source epochs
    and target epochs cover the same time period.
    
    Points in the target epoch falling before the source epoch start time will 
    contain the quality flag of the earliest entry in the quality flag variable.
    
    Points in the target epoch falling after the source epoch end time will 
    contain the quality flag of the last entry in the quality flag variable.

    Parameters
    ----------
        target: str
            Tplot variable name with the target epoch times

        source: str
            Tplot variable name with the source epoch times (ie: root quality flag variable)

        tag: str
            Tplot variable name suffix for new quality flag variable
    
    Returns
    ----------
        error: int
            Error status
            0 for nominal execution
            1 if the source and target epoch ranges are completely disjoint
                or do not overlap by at least 90% of the target time range.
                No new tplot variables are created in this instance.    
    """
    
    qfd = get_data(source)
    src = qfd.times
    tar = get_data(target).times.copy()

    # Check for valid ranges
    if (tar[-1] < src[0]) or (tar[0] > src[-1]):
        print("Epoch ranges are disjoint.")
        return 1
    else:
        tar_dur = tar[-1] - tar[0]
        src_overlap = src[(src >= tar[0]) & (src <= tar[-1])]
        overlap_dur = src_overlap[-1] - src_overlap[0]
        if overlap_dur/tar_dur < 0.9:
            print("Bad epoch ranges.")
            return 1

    newY = np.full_like(tar, qfd.y[0], dtype=qfd.y.dtype)
    for i in range(len(src) - 1):
        mask = (tar >= src[i]) & (tar < src[i+1])
        newY[mask] = qfd.y[i].copy()
    mask = tar >= src[-1]
    newY[mask] = qfd.y[-1].copy()

    newData = {'x':tar, 'y':newY}
    store_data(source+tag, newData)
    return 0
