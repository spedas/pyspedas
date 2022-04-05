
import logging
from time import time

from pyspedas import time_double, mms
from pyspedas.mms.particles.mms_part_products import mms_part_products

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def mms_part_getspec(instrument='fpi', probe='1', species='e', data_rate='fast', 
    trange=None, output=['energy', 'theta', 'phi', 'pa', 'gyro'], units='eflux', energy=None,
    phi=None, theta=None, pitch=None, gyro=None, mag_data_rate=None, scpot_data_rate=None, fac_type='mphigeo',
    center_measurement=False, spdf=False, correct_photoelectrons=False, 
    internal_photoelectron_corrections=False, disable_photoelectron_corrections=False, zero_negative_values=False,
    regrid=[32, 16], no_regrid=False):
    """
    Generate spectra and moments from 3D MMS particle data

    Parameters
    ----------
        trange: list of str
            Time range

        units: str
            Specify units of output variables; must be 'eflux' to calculate moments

            valid options:
            'flux'   -  # / (cm^2 * s * sr * eV)
            'eflux'  -  eV / (cm^2 * s * sr * eV)  <default>
            'df_cm'  -  s^3 / cm^6
            'df_km'  -  s^3 / km^6

        species: str
            Specify the species of the input tplot variable

        data_rate: str
            Data rate of the input data

        instrument: str
            Instrument (FPI or HPCA)

        probe: int or str
            Spacecraft probe #

        output: str or list of str
            Output variables; options: 
                'energy': energy spectrograms
                'theta': theta spectrograms
                'phi': phi spectrograms
                'pa': pitch-angle spectrograms
                'gyro': gyro-phase spectrograms
                'moments': plasma moments

        energy: list of float
            Energy range [min, max], in eV

        phi: list of float
            Phi range [min, max], in degrees

        theta: list of float
            Theta range [min, max], in degrees

        pitch: list of float
            Pitch-angle range [min, max], in degrees

        gyro: list of float
            Gyro-angle range [min, max], in degrees

        mag_name: str
            Tplot variable containing magnetic field data for
            moments and FAC transformations

        pos_name: str
            Tplot variable containing spacecraft position for
            FAC transformations

        sc_pot_name: str
            Tplot variable containing spacecraft potential data
            for moments corrections

        fac_type: str
            Field aligned coordinate system variant; default: 'mphigeo'
            options: 'phigeo', 'mphigeo', 'xgse'

        correct_photoelectrons: bool
            Flag to correct FPI data for photoelectrons 
            (defaults to True for FPI electron data - disable with the parameter below)

        disable_photoelectron_corrections: bool
            Flag to disable FPI photoelectron corrections

        internal_photoelectron_corrections: bool
            Apply internal photoelectron corrections

        zero_negative_values: bool
            Turn negative values to 0 after doing the photoelectron corrections (DES)

    Returns
    ----------
        Creates tplot variables containing spectrograms and moments

    """

    start_time = time()

    if trange is None:
        # test data for development
        trange = ['2015-10-16/13:06', '2015-10-16/13:07']
        # data_rate = 'brst'

    if mag_data_rate is None:
        if data_rate == 'brst':
            mag_data_rate = 'brst'
        else:
            mag_data_rate = 'srvy'

    if scpot_data_rate is None:
        if data_rate == 'brst':
            scpot_data_rate = 'brst'
        else:
            scpot_data_rate = 'fast'

    instrument = instrument.lower()

    # HPCA is required to be at the center of the accumulation interval
    # due to assumptions made in mms_get_hpca_dist
    if instrument == 'hpca' and center_measurement == False:
        center_measurement = True
    
    if instrument == 'fpi':
        data_vars = mms.fpi(datatype='d'+species+'s-dist', probe=probe, data_rate=data_rate, trange=trange, time_clip=True, center_measurement=center_measurement, spdf=spdf)
    elif instrument == 'hpca':
        # for HPCA, 'fast' should be 'srvy'
        if data_rate == 'fast':
            data_rate = 'srvy'
        # 'i' and 'e' are only valid for FPI
        if species in ['i', 'e']:
            species = 'hplus'
        data_vars = mms.hpca(datatype='ion', probe=probe, data_rate=data_rate, trange=trange, time_clip=True, center_measurement=center_measurement, get_support_data=True, spdf=spdf)
    else:
        logging.error('Error, unknown instrument: ' + instrument + '; valid options: fpi, hpca')
        return

    if data_vars is None or len(data_vars) == 0:
        logging.error('Error, no data loaded.')
        return None

    if not isinstance(probe, list):
        probe = [probe]

    if instrument == 'fpi' and species == 'e' and 'moments' in output and not disable_photoelectron_corrections:
        correct_photoelectrons = True

    support_trange = [time_double(trange[0])-60.0, time_double(trange[1])+60.0]

    # load state data (needed for coordinate transformations and field-aligned coordinates)
    pos_vars = mms.mec(probe=probe, trange=support_trange, time_clip=True, spdf=spdf)

    if len(pos_vars) == 0:
        logging.error('Error, no state data loaded.')
        return

    mag_vars = mms.fgm(probe=probe, trange=support_trange, data_rate=mag_data_rate, time_clip=True, spdf=spdf)

    if len(mag_vars) == 0:
        logging.error('Error, no magnetic field data loaded.')
        return

    scpot_vars = mms.edp(probe=probe, trange=support_trange, level='l2', spdf=spdf, data_rate=scpot_data_rate, datatype='scpot', varformat='*_edp_scpot_*')

    out_vars = []

    for prb in probe:
        prb_str = str(prb)
        mag_name = 'mms'+prb_str+'_fgm_b_gse_'+mag_data_rate+'_l2_bvec'
        pos_name = 'mms'+prb_str+'_mec_r_gse'

        if instrument == 'fpi':
            tname = 'mms'+prb_str+'_d'+species+'s_dist_'+data_rate
        elif instrument == 'hpca':
            tname = 'mms'+prb_str+'_hpca_'+species+'_phase_space_density'

        scpot_variable = 'mms'+prb_str+'_edp_scpot_'+scpot_data_rate+'_l2'

        new_vars = mms_part_products(tname, species=species, instrument=instrument, probe=prb, data_rate=data_rate,
                          output=output, units=units, energy=energy, phi=phi, theta=theta, pitch=pitch, gyro=gyro,
                          mag_name=mag_name, pos_name=pos_name, fac_type=fac_type, sc_pot_name=scpot_variable,
                          correct_photoelectrons=correct_photoelectrons, zero_negative_values=zero_negative_values,
                          internal_photoelectron_corrections=internal_photoelectron_corrections,
                          disable_photoelectron_corrections=disable_photoelectron_corrections, regrid=regrid,
                          no_regrid=no_regrid)
        
        if new_vars is None:
            continue

        out_vars = out_vars + new_vars

    logging.info('Finished; time to run: ' + str(round(time()-start_time, 1)) + ' seconds.')
    
    return out_vars