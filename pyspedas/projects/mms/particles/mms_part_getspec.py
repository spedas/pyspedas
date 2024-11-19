import logging
from time import time
from pyspedas.projects import mms
from pyspedas.projects.mms.particles.mms_part_products import mms_part_products
from pytplot import time_double
logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_part_getspec(instrument='fpi',
                     probe='1',
                     species='e',
                     data_rate='fast',
                     trange=None,
                     output=['energy', 'theta', 'phi', 'pa', 'gyro'],
                     units='eflux',
                     energy=None,
                     phi=None,
                     theta=None,
                     pitch=None,
                     gyro=None,
                     mag_name=None,
                     mag_data_rate=None,
                     pos_name=None,
                     sc_pot_name=None,
                     sc_pot_data_rate=None,
                     fac_type='mphigeo',
                     center_measurement=False,
                     spdf=False,
                     correct_photoelectrons=False,
                     internal_photoelectron_corrections=False,
                     disable_photoelectron_corrections=False,
                     zero_negative_values=False,
                     regrid=[32, 16],
                     no_regrid=False,
                     prefix='',
                     suffix=''):
    """
    Generate spectra and moments from 3D MMS particle data

    Parameters
    ----------
        trange: list of str
            Time range

        units: str
            Specify units of output variables; must be 'eflux' to calculate moments.   Valid options::

                'flux'   -  # / (cm^2 * s * sr * eV)
                'eflux'  -  eV / (cm^2 * s * sr * eV)  <default>
                'df_cm'  -  s^3 / cm^6
                'df_km'  -  s^3 / km^6

            Default: 'eflux'

        species: str
            Specify the species of the input tplot variable (Default: 'e')

        data_rate: str
            Data rate of the input data (Default: 'fast')

        instrument: str
            Instrument (FPI or HPCA)

        probe: int or str
            Spacecraft probe # (Default: 1)

        output: str or list of str
            Output variables; options::

                'energy': energy spectrograms
                'theta': theta spectrograms
                'phi': phi spectrograms
                'pa': pitch-angle spectrograms
                'gyro': gyro-phase spectrograms
                'moments': plasma moments

            Default: ['energy', 'theta', 'phi', 'pa', 'gyro']

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

        mag_data_rate: str
            Data rate to use when loading the spacecraft potential data ('fast', 'srvy' or 'brst')
            If not given, defaults to value of 'data_rate'.

        pos_name: str
            Tplot variable containing spacecraft position for
            FAC transformations. If not given, defaults to 'mmsN_mec_r_gse'

        sc_pot_name: str
            If set, overrides default sc_pot variable name constructed from sc_pot_data_rate below.
            Default: None

        sc_pot_data_rate: str
            Data rate to use when loading the spacecraft potential data ('fast', 'srvy' or 'brst')
            If not given, defaults to value of 'data_rate'.

        fac_type: str
            Field aligned coordinate system variant; options::

                'phigeo'
                'mphigeo'
                'xgse'

            Default: 'mphigeo'

        correct_photoelectrons: bool
            Flag to correct FPI data for photoelectrons 
            (defaults to True for FPI electron data - disable with the parameter below)

        disable_photoelectron_corrections: bool
            Flag to disable FPI photoelectron corrections

        internal_photoelectron_corrections: bool
            Apply internal photoelectron corrections

        zero_negative_values: bool
            Turn negative values to 0 after doing the photoelectron corrections (DES)

        regrid: array of int
            Dimensions for regridded data array (see no_regrid flag below)
            Default: [32,16]

        no_regrid: bool
            Flag to disable regridding of data array

        prefix: str
            Prefix for output tplot variables. Default: ''

        suffix: str
            Suffix for output tplot variables. Default: ''

    Returns
    -------
    None
       Creates tplot variables containing spectrograms and moments

    """

    start_time = time()

    if trange is None:
        logging.error('Time range not specified; please specify time range using the trange keyword.')
        return

    if mag_data_rate is None:
        if data_rate == 'brst':
            mag_data_rate = 'brst'
        else:
            mag_data_rate = 'srvy'

    if sc_pot_data_rate is None:
        if data_rate == 'brst':
            sc_pot_data_rate = 'brst'
        else:
            sc_pot_data_rate = 'fast'

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

    scpot_vars = mms.edp(probe=probe, trange=support_trange, level='l2', spdf=spdf, data_rate=sc_pot_data_rate, datatype='scpot', varformat='*_edp_scpot_*')

    out_vars = []

    for prb in probe:
        prb_str = str(prb)

        if mag_name is None or mag_name == '':
            mag_name = 'mms'+prb_str+'_fgm_b_gse_'+mag_data_rate+'_l2_bvec'
        else:
            logging.info("Using non-default variable %s for mag data",mag_name)

        if pos_name is None or pos_name == '':
            pos_name = 'mms'+prb_str+'_mec_r_gse'
        else:
            logging.info("Using non-default variable %s for position data",pos_name)

        if sc_pot_name is None or sc_pot_name == '':
            sc_pot_name = 'mms' + prb_str + '_edp_scpot_' + sc_pot_data_rate + '_l2'
        else:
            logging.info('Using non-default variable %s for sc_pot data', sc_pot_name)

        if instrument == 'fpi':
            tname = 'mms'+prb_str+'_d'+species+'s_dist_'+data_rate
        elif instrument == 'hpca':
            tname = 'mms'+prb_str+'_hpca_'+species+'_phase_space_density'

        new_vars = mms_part_products(tname, species=species, instrument=instrument, probe=prb, data_rate=data_rate,
                          output=output, units=units, energy=energy, phi=phi, theta=theta, pitch=pitch, gyro=gyro,
                          mag_name=mag_name, pos_name=pos_name, fac_type=fac_type, sc_pot_name=sc_pot_name,
                          correct_photoelectrons=correct_photoelectrons, zero_negative_values=zero_negative_values,
                          internal_photoelectron_corrections=internal_photoelectron_corrections,
                          disable_photoelectron_corrections=disable_photoelectron_corrections, regrid=regrid,
                          no_regrid=no_regrid, prefix=prefix, suffix=suffix)
        
        if new_vars is None:
            continue

        out_vars = out_vars + new_vars

    logging.info('Finished; time to run: ' + str(round(time()-start_time, 1)) + ' seconds.')
    
    return out_vars
