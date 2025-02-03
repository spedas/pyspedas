import logging
import pyspedas
import pyspedas.projects.themis
from pytplot import data_exists
from pytplot import time_double
from pyspedas.projects.themis.state_tools.spinmodel.spinmodel import get_spinmodel
import pytplot


def load_needed(trange_loaded,
                trange_needed,
                tolerance=0.0):
    """
    Given a time range of loaded data, and the time range needed, determine if
    a support variable needs to be reloaded.  A small amount of extrapolation is considered
    acceptable, so the time comparisons are done with a user-specified tolerance.

    Parameters:
        trange_loaded: list of float
            Start and end times (Unix times) for support variable currently loaded.

        trange_needed: list of float
            Start and end times (Unix times) for support variable needed to support desired operation.

        tolerance: float
            A duration, in seconds, for which extrapolation from currently loaded data is considered valid.
    """
    st = trange_loaded[0] - tolerance
    et = trange_loaded[1] + tolerance
    if (trange_needed[0] > st) and (trange_needed[1] < et):
        return False
    else:
        return True


def autoload_support(varname=None,
                     trange=None,
                     probe=None,
                     spinaxis: bool = False,
                     spinmodel: bool = False,
                     slp: bool = False):
    """
    Automatically load THEMIS support data required to cover a given probe or time range.

    Parameters:
        varname: str (optional)
            Name of a tplot variable for which calibration, cotrans, or other operation requiring
                support data is needed.  The trange and probe arguments are optional if this argument
                is provided.

        trange: list of Unix times or time strings
            Start and end times (in either string or Unix time format) for which support data is needed.
            Required if varname not specified.

        probe: str (optional)
            A single letter probe identifier.  Required if varname not specified, and spinaxis or spinmodel
                support data is requested.

        spinaxis: bool
            If True, the spin axis variables from the state CDF are examined to see if state needs to
            be reloaded.

        spinmodel: bool
            If True, the spin model produced from the state CDF is examined to see if state needs to
            be reloaded.

        slp: bool
            If True, the tplot variables holding sun and moon positions and lunar coordinate system axes
            are examined to see if the SLP data needs to be reloaded.


    """
    if varname is not None:
        trange = pytplot.get_timespan(varname)
    elif trange is None:
        logging.error("Must specify either a tplot name or a time range in order to load support data")
        return
    elif (probe is None) and (spinaxis or spinmodel):
        logging.error("Must specify either a tplot name or a probe in order to load spin axis or spin model data")
        return

    # Validate varname if present
    if (varname is not None) and not (data_exists(varname)):
        logging.error("tplot variable name " + varname + " not found.")
        return

    # Set probe name (if needed)
    if spinaxis or spinmodel:
        if probe is None:
            probe = varname[2]

    # Set time range (if needed)
    if trange is None:
        trange_needed = pytplot.get_timespan(varname)
    else:
        if isinstance(trange[0], str):
            trange_needed = time_double(trange)
        else:
            trange_needed = trange

    do_state = False
    do_slp = False
    slop = 120.0  # Tolerance (seconds) for determining if existing data covers desired range

    # Does spin model cover desired time interval?
    if spinmodel:
        sm = get_spinmodel(probe, correction_level=1, quiet=True)
        if sm is None:
            do_state = True
        else:
            sminfo = sm.get_timerange()
            trange_loaded = sminfo
            if load_needed(trange_loaded, trange_needed, tolerance=slop):
                do_state = True

    # Do spin axis variables exist, and cover desired time interval?

    if spinaxis:
        v1 = "th" + probe + "_spinras"
        v2 = "th" + probe + "_spindec"
        v3 = "th" + probe + "_spinras_corrected"
        v4 = "th" + probe + "_spindec_corrected"

        # Check uncorrected variables
        if not (data_exists(v1)) or not (data_exists(v2)):
            do_state = True
        else:
            v1_tr = pytplot.get_timespan(v1)
            v2_tr = pytplot.get_timespan(v2)
            if (load_needed(v1_tr, trange_needed, tolerance=slop) or
                    load_needed(v2_tr, trange_needed, tolerance=slop)):
                do_state = True

        # Check corrected variables.  They may be unavailable even if state is reloaded,
        # so only force a reload if one of the variables exists, but doesn't cover the
        # needed time range.

        if data_exists(v3):
            v3_tr = pytplot.get_timespan(v3)
            if load_needed(v3_tr, trange_needed, tolerance=slop):
                do_state = True

        if data_exists(v4):
            v4_tr = pytplot.get_timespan(v4)
            if load_needed(v4_tr, trange_needed, tolerance=slop):
                do_state = True

    # Check SLP variables.  They must all exist, and cover the desired time range, or
    # reload is necessary.

    if slp:
        v1 = 'slp_lun_att_x'
        v2 = 'slp_lun_att_z'
        v3 = 'slp_lun_pos'
        v4 = 'slp_sun_pos'
        if not (data_exists(v1) and data_exists(v2) and data_exists(v3) and data_exists(v4)):
            do_slp = True
        else:
            v1_tr = pytplot.get_timespan(v1)
            v2_tr = pytplot.get_timespan(v2)
            v3_tr = pytplot.get_timespan(v3)
            v4_tr = pytplot.get_timespan(v4)
            if (load_needed(v1_tr, trange_needed, tolerance=slop)
                    or load_needed(v2_tr, trange_needed, tolerance=slop)
                    or load_needed(v3_tr, trange_needed, tolerance=slop)
                    or load_needed(v4_tr, trange_needed, tolerance=slop)):
                do_slp = True

    # Perform the needed updates
    if do_slp:
        pyspedas.projects.themis.slp(trange=trange_needed)
    if do_state:
        pyspedas.projects.themis.state(probe=probe, trange=trange_needed, get_support_data=True)
