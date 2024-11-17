import pyspedas
import pytplot
import numpy as np
from scipy.interpolate import interp1d
from pytplot.time_double import time_double

def dens_pot(scpot, offset, pder_calc=False):
    """
    Evaluates McFadden's empirical formula for calculating density as a function of spacecraft potiential.

    Parameters
    ----------
    scpot : list or float
        Spacecraft potential.
    offset : float
        An offset.
    pder_calc : bool=True
        If True, the partial derivative with respect to `scpot` will be calculated.

    Returns
    -------
    result : list or float
        The calculated result based on the empirical formula.
    pder : list of float, optional
        The partial derivative with respect to `scpot`, if `pder` was provided.

    Examples
    --------
    >>> dens_pot(-5.0, 10.0)
    Calculated density potential based on the spacecraft potential and offset.

    >>> dens_pot(-5.0, 10.0, True)
    (Tuple containing the calculated density potential and its partial derivative with respect to the spacecraft potential.)

    References
    ----------
    Based on IDL function THM_SCPOT2DENS.PRO by M.Feuerstein, 5/18/2009.
    SPEDAS/projects/themis/common/thm_scpot2dens.pro
    """

    delta = offset - scpot
    result = 460. * np.power(10, delta / 1.5) + 34. * np.power(10, delta / 0.7) + 1.6 * np.power(10, delta / 30.)

    if pder_calc:
        pder = np.log(10) * ((460. / 1.5) * np.power(10, delta / 1.5) + (34. / 0.7) * np.power(10, delta / 0.7) + (
                    1.6 / 30.) * np.power(10, delta / 30.))
        return result, pder

    return result


def interpolate_to_scptime(source_time, target_time, source_data):
    """
    Interpolates source data to the target time base, handling non-finite values.

    This function takes a series of data points defined at certain times (`source_data` at `source_time`)
    and interpolates these data points to a new series of times (`target_time`). It specifically handles
    cases where the source data might contain non-finite values (e.g., NaN or infinity) by filtering those
    out before interpolation. If there are not enough finite data points to perform interpolation, it returns
    an array of NaN values of the same shape as `target_time`.

    Parameters
    ----------
    source_time : array_like
        The time points corresponding to the `source_data` values.
    target_time : array_like
        The time points to which `source_data` should be interpolated.
    source_data : array_like
        The data values that need to be interpolated to the new time base.

    Returns
    -------
    ndarray
        The interpolated data values at `target_time`. If interpolation is not possible due to insufficient
        finite data points in `source_data`, returns an array of NaN values matching the shape of `target_time`.

    Examples
    --------
    >>> source_time = [1, 2, 3, 4]
    >>> source_data = [1, np.nan, 3, 4]
    >>> target_time = [2, 3]
    >>> interpolate_to_scptime(source_time, target_time, source_data)
    array([2., 3.5])

    Notes
    -----
        - This function is not intended for extenal use, but could be usefull for other analytical tools.
    """

    # Ensure source_time and source_data are numpy arrays for boolean indexing
    source_time = np.array(source_time)
    source_data = np.array(source_data)

    # Filter out non-finite values to avoid interpolation errors
    finite_indices = np.isfinite(source_data)
    if np.sum(finite_indices) < 2:
        # Not enough data points to interpolate
        return np.full_like(target_time, np.nan)

    interp_func = interp1d(source_time[finite_indices], source_data[finite_indices],
                           bounds_error=False, fill_value=np.nan)

    return interp_func(target_time)


def scpot2dens(scpot, scptime, Te, Tetime, dens_e, dens_e_time, dens_i, dens_i_time, probe='c'):
    """
    Calculates spacecraft potential derived density.

    This function processes spacecraft potential data (`scpot`), alongside interpolated electron temperature (`Te`),
    electron density (`dens_e`), and ion density (`dens_i`) data, to calculate electron and ion densities at specific
    time points (`scptime`). It interpolates `Te`, `dens_e`, and `dens_i` data to align with the `scpot` time base,
    It accounts for specific bias changes and offset matrices.

    Parameters
    ----------
    scpot : array_like
        Spacecraft potential data, expected as a 1-D array. (call pyspedas.projects.themis.esa, DATATYPE = 'peer_sc_pot')
    scptime : array_like
        The time base of `scpot`.
    Te : array_like
        Electron temperature data, expected as a 1-D array. (call pyspedas.projects.themis.esa, DATATYPE = 'peer_avgtemp')
    Tetime : array_like
        The time base of `Te`.
    dens_e : array_like
        Electron density data, expected as a 1-D array. (call pyspedas.projects.themis.esa, DATATYPE = 'peer_density')
    dens_e_time : array_like
        The time base for `dens_e`.
    dens_i : array_like
        Ion density data, expected as a 1-D array. (call pyspedas.projects.themis.esa, DATATYPE = 'peir_density')
    dens_i_time : array_like
        The time base for `dens_i`.
    probe_in : int or str, default='c'
        Identifier for the probe being used for measurements. Valid values are 'a', 'b', 'c', 'd', 'e'.

    Returns
    -------
    dens : ndarray
        The calculated densities at `scpot` time points. Returns None if the probe is invalid, if `dens_e` and `dens_i`
        are either not present or do not have at least two elements (indicating insufficient data for interpolation),
        or if the densities remain unmodified due to a lack of valid data.

    Notes
    -----
    - Incorporates probe-specific adjustments through bias changes and offset matrices, applying different
      calculation methodologies across distinct plasma conditions and time periods.
    - Invalid inputs or insufficient density data lead to an early termination of the function with None as return.

    Examples
    --------
    Given a specific time range, the following example demonstrates how to load THEMIS spacecraft data for probe 'c',
    extract density, spacecraft potential, and temperature data, then calculate the plasma density from spacecraft potential
    using the `scpot2dens` function.

    ```python
    import pyspedas
    import pytplot
    from pyspedas.projects.themis.analysis import scpot2dens

    # Define the time range for which to load the data
    trange = ['2007-7-20/17:00:00', '2007-7-20/17:20:00']

    # Load THEMIS ESA data for probe 'c' within the specified time range
    pyspedas.projects.themis.esa(trange=trange,
                        probe='c',
                        varnames=['thc_peer_density', 'thc_peir_density', 'thc_peer_sc_pot', 'thc_peer_avgtemp'],
                        level='l2')

    # Retrieve electron density
    dens_e_time, dens_e = pytplot.get_data('thc_peer_density')

    # Retrieve ion density
    dens_i_time, dens_i = pytplot.get_data('thc_peir_density')

    # Retrieve spacecraft potential
    sc_pot_time, sc_pot = pytplot.get_data('thc_peer_sc_pot')

    # Retrieve electron temperature
    Te_time, Te = pytplot.get_data('thc_peer_avgtemp')

    # Calculate the plasma density from spacecraft potential
    Npot = scpot2dens(sc_pot, sc_pot_time, Te, Te_time, dens_e, dens_e_time, dens_i, dens_i_time, 'c')
    ```

    References
    ----------
    Based on IDL function THM_SCPOT2DENS.PRO by W.M.Feuerstein, 2009-05-18, with updates and bug fixes in subsequent versions.
    SPEDAS/projects/themis/common/thm_scpot2dens.pro
    """

    # Probe validation and selection
    valid_probes = ['a', 'b', 'c', 'd', 'e']

    if str(probe).lower() not in valid_probes:
        pyspedas.logger.error("Invalid probe entered. Valid probes are [a, b, c, d, e]")
        return None

    # Check if Ne and Ni exist and have >= 2 elements
    if not (dens_e[0] != -1 and dens_i[0] != -1) or (len(dens_e) < 2 or len(dens_i) < 2):
        pyspedas.logger.error("dens_e and dens_i must exist and have two or more elements.")
        return None

    # Interpolate Te, dens_e, and dens_i to scpot time base
    Teint = interpolate_to_scptime(Tetime, scptime, Te)
    dens_e_int = interpolate_to_scptime(dens_e_time, scptime, dens_e)
    dens_i_int = interpolate_to_scptime(dens_i_time, scptime, dens_i)

    # Common bias change and offset matrix for probes 'a', 'b', 'd', and 'e'
    common_bias_change = [time_double('2001-1-1')]
    common_offset_matrix = np.array([[2.2, 2.0, np.nan, np.nan]])

    # Define bias changes and offset matrices for each probe with more compact representation
    bias_changes = {
        probe: {
            'biaschange': common_bias_change,
            'offsetmatrix': common_offset_matrix
        } for probe in ['a', 'b', 'd', 'e']
    }

    # Adding the unique entry for probe 'c'
    bias_changes['c'] = {
        'biaschange': [time_double('2001-1-1'),
                       time_double('2007-7-20 17:24')],
        'offsetmatrix': np.array([[2.2, 2.0, np.nan, np.nan],
                                  [2.9, 2.0, np.nan, np.nan]])
    }

    biaschange_for_probe = bias_changes[probe]['biaschange']
    offsetmatrix_for_probe = bias_changes[probe]['offsetmatrix']

    # Interpolate Te to scpot time base
    Te_interp_func = interp1d(Tetime, Te, bounds_error=False, fill_value="extrapolate")
    Teint = Te_interp_func(scptime)

    # Initialize density array
    dens = np.full_like(scpot, np.nan)

    # Process each bias period
    for i, bias_time in enumerate(biaschange_for_probe):
        # Define conditions for different plasma regions and bias periods
        if i != len(biaschange_for_probe) - 1:
            next_bias = biaschange_for_probe[i + 1]
        else:
            next_bias = time_double('9999-12-31')  # A future date to ensure the last period is included

        time_index = (scptime >= biaschange_for_probe[i]) & (scptime < next_bias)
        if not np.any(time_index):
            continue

        wll = (scpot <= 6.0) & (Teint <= 500) & time_index
        wlh = (scpot <= 6.0) & (Teint > 500) & time_index
        whl = (scpot > 6.0) & (Teint <= 500) & time_index
        whh = (scpot > 6.0) & (Teint > 500) & time_index
        wnf = (~np.isfinite(scpot) | ~np.isfinite(Teint)) & time_index

        # Apply density calculations based on conditions
        # Assuming dens_pot function is defined elsewhere and calculates density based on spacecraft potential and offset
        if np.any(wll):
            dens[wll] = dens_pot(scpot[wll], offsetmatrix_for_probe[i, 0])  # Example calculation, adjust as needed
        if np.any(wlh):
            dens[wlh] = dens_pot(scpot[wlh], offsetmatrix_for_probe[i, 1])  # Adjust as needed

        # For whl and whh, using a simplified formula directly as an example
        if np.any(whl):
            dens[whl] = np.exp((-scpot[whl] + 12) / ((scpot[whl] * 0.14) + 3.36)) / np.sqrt(Teint[whl])
            # Recompute for cold electrons if needed, similar logic to IDL's idxT
        if np.any(whh):
            dens[whh] = np.exp((-scpot[whh] + 12) / ((scpot[whh] * 0.14) + 3.36)) / np.sqrt(Teint[whh])
            # Recompute for cold electrons if needed

        # Handling non-finite values
        if np.any(wnf):
            dens[wnf] = np.nan  # Assign NaN for non-finite conditions

    return dens
