import pyspedas
import numpy as np
from scipy.interpolate import interp1d
from pyspedas.tplot_tools.time_double import time_double
from pyspedas.projects.themis.analysis.scpot2dens import interpolate_to_scptime

# Nishimura version
def scpot2dens_nishimura(scpot, scptime, vth, vth_time, dens_i, dens_i_time, pos_gsm, pos_gsm_time, probe='a', ion_density_threshold=40, no_interp=False):
    """
    Calculates spacecraft potential derived density, using Nishimura formula, as in the IDL SPEDAS SCPOT2DENS_OPT_N

    This function processes spacecraft potential data (`scpot`), alongside interpolated electron thermal velocity (`Vth`),
    ion density (`dens_i`) data and spacecraft position (`pos`), to calculate electron and ion densities at specific
    time points (`scptime`). It interpolates all data to the `scpot` time base. If no_interp is set, only the position 
    data is interpolated. Ion density is used to flag bad data; the calculation is expected to fail for high Ion density (Gt 40cm^(-3))

    Parameters
    ----------
    scpot : array_like
        Spacecraft potential data, expected as a 1-D array. (call pyspedas.projects.themis.esa, DATATYPE = 'peer_sc_pot')
    scptime : array_like
        The time base of `scpot`.
    vth : array_like
        Electron thermal velocity data, expected as a 1-D array. (call pyspedas.projects.themis.esa, DATATYPE = 'peer_vthermal')
    vth_time : array_like
        The time base of `vth`.
    dens_i : array_like
        Ion density data, expected as a 1-D array. (call pyspedas.projects.themis.esa, DATATYPE = 'peir_density')
    dens_i_time : array_like
        The time base for `dens_i`.
    pos_gsm: array_like
        Spacecraft position in GSM (or any earth-centered coordinates.).
    pos_gsm_time: array_like
        The time base of `pos_gsm`
    probe : int or str, default='a'
        Identifier for the probe being used for measurements. Valid values are 'a', 'b', 'c', 'd', 'e'.
    ion_density_threshold: Scalar, int or float, default=40
        Threshold for ion density, above which, data is set to 'NaN'
    no_interp : Boolean
        If True, then all of the probe ESA arrays are the same (typical for THEMIS ESA data), no need to interpolate times.
        Position data is always interpolated

    Returns
    -------
    dens : ndarray
        The calculated densities at `scpot` time points. Returns None if the probe is invalid, if `dens_i`
        is not present or do not have at least two elements (indicating insufficient data for interpolation, 
        for no_interp=False)

    Notes
    -----
    - Incorporates probe-specific adjustments
    - Invalid inputs or insufficient data lead to an early termination of the function with None as return.

    Examples
    --------
    Given a specific time range, the following example demonstrates how to load THEMIS spacecraft data for probe 'a',
    extract density, spacecraft potential, and velocity data, then calculate the plasma density from spacecraft potential
    using the `scpot2dens` function.



    >>> import pyspedas
    >>> from pyspedas.projects.themis import scpot2dens_nishimura
    >>> from pyspedas import get_data
    >>>
    >>> # Define the time range for which to load the data
    >>> trange = ['2017-07-20', '2017-07-20']
    >>>
    >>> # Load THEMIS ESA data for probe 'a' within the specified time range
    >>> pyspedas.projects.themis.esa(trange=trange,
    >>>                     probe='a',
    >>>                     varnames=['tha_peir_density', 'tha_peer_sc_pot', 'tha_peer_vthermal'],
    >>>                     level='l2')
    >>>
    >>> # Load position data
    >>> pyspedas.projects.themis.state(probe='a', trange=trange)
    >>> pos_data = get_data('tha_pos_gsm')
    >>> pos_gsm_time = pos_data.times
    >>> pos_gsm = pos_data.y
    >>>
    >>> # Retrieve ion density
    >>> dens_i_time, dens_i = get_data('tha_peir_density')
    >>>
    >>> # Retrieve spacecraft potential
    >>> sc_pot_time, sc_pot = get_data('tha_peer_sc_pot')
    >>>
    >>> # Retrieve electron velocity
    >>> vth_time, vth = get_data('tha_peer_vthermal')
    >>>
    >>> # Calculate the plasma density from spacecraft potential, ESA datatimes are all the same
    >>> Npot = scpot2dens_nishimura(sc_pot, sc_pot_time, vth, vth_time, dens_i, dens_i_time, pos_gsm, pos_gsm_time, probe='a', no_interp=True)

    References
    ----------
    Based on IDL function THM_SCPOT2DENS_OPT_N.PRO by Toshi Nishimura@UCLA/NAGOYA, 05/02/2009 (toshi at atmos.ucla.edu)
    SPEDAS/projects/themis/common/thm_scpot2dens_opt_n.pro
    """

    # Probe validation and selection
    valid_probes = ['a', 'b', 'c', 'd', 'e']

    if str(probe).lower() not in valid_probes:
        pyspedas.logger.error("Invalid probe entered. Valid probes are [a, b, c, d, e]")
        return None

    # Check if Ni exists and have >= 2 elements if no_interp is False
    if no_interp == False:
        if len(dens_i) < 2 or dens_i[0] == -1:
            pyspedas.logger.error("dens_i must exist and have two or more elements.")
            return None
    else: #Can have a single element if not interpolating
        if dens_i[0] == -1:
            pyspedas.logger.error("dens_i must exist.")
            return None            

# Get position from earth center in KM
    if len(pos_gsm) < 2:
        pyspedas.logger.error("GSM position must exist.")
        return None
    R = np.linalg.norm(pos_gsm, axis = 1)/6371.2
    R_int = interpolate_to_scptime(pos_gsm_time, scptime, R)
    
    if no_interp == False:
        # Interpolate vth and dens_i to scpot time base
        vth_int = interpolate_to_scptime(vth_time, scptime, vth)
        dens_i_int = interpolate_to_scptime(dens_i_time, scptime, dens_i)
    else:
        # Or not
        vth_int = vth
        dens_i_int = dens_i

    #Get vthdata2
    vthdata2 = vth_int*(1-(-1/(1+np.exp(-2*(R_int-4)))+1))+10**4*(-1/(1+np.exp(-2*(R_int-4)))+1)

    #scpn is the negative potential
    scpn = -scpot

    #Get density
    if probe == 'a':
        Ne_scpot = (
            10**(scpn/22.0) * 20000. +
            10**(scpn/ 5.0) * 160000. +
            10**(scpn/ 2.0) * 15000000.0 +
            10**(scpn/ 0.4) * 1.5e12
        ) / vthdata2

    elif probe == 'b':
        Ne_scpot = (
            10**(scpn/25.5) * 16500. +
            10**(scpn/ 2.0) * 3000000.0 +
            10**(scpn/ 0.4) * 1.5e12
        ) / vthdata2

    elif probe == 'c':
        Ne_scpot = (
            10**(scpn/26.0) * 22000. +
            10**(scpn/ 2.0) * 3000000.0 +
            10**(scpn/ 0.25) * 1e14
        ) / vthdata2

    elif probe == 'd':
        Ne_scpot = (
            10**(scpn/25.5) * 20000. +
            10**(scpn/  5.0) * 30000. +
            10**(scpn/  2.0) * 10000000.0 +
            10**(scpn/  0.2) * 5e15
        ) / vthdata2

    elif probe == 'e':
        Ne_scpot = (
            10**(scpn/25.5) * 20000. +
            10**(scpn/  5.0) * 30000. +
            10**(scpn/  2.0) * 10000000.0 +
            10**(scpn/  0.2) * 3e15
        ) / vthdata2

    #That's all, check the ion density
    Ne_scpot[Ne_scpot > ion_density_threshold] = np.nan
    
    return Ne_scpot
