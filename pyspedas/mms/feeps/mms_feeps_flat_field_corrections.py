'''
 PURPOSE:
       Apply flat field correction factors to FEEPS ion/electron data;
       correct factors are from the gain factor found in:
       
           FlatFieldResults_V3.xlsx
           
       from Drew Turner, 1/19/2017

 NOTES:
 
   From Drew Turner, 1/18/17:
       Here are the correction factors that we need to apply to the current 
       ION counts/rates/fluxes in the CDF files.  
       NOTE, THIS IS A DIFFERENT TYPE OF CORRECTION THAN THAT FOR THE ELECTRONS!  
       These shifts should be applied to the counts/rates/fluxes data EYE-BY-EYE on each spacecraft.  
       These are multiplication factors (i.e., Jnew = Jold * Gcorr). 
       For those equations, Jold is the original count/rate/flux array and
       Jnew is the corrected version of the arrays using the factors listed below.
       
        MMS1:
        Top6: Gcorr = 0.7
        Top7: Gcorr = 2.5
        Top8: Gcorr = 1.5
        Bot6: Gcorr = 0.9
        Bot7: Gcorr = 1.2
        Bot8: Gcorr = 1.0

        MMS2:
        Top6: Gcorr = 1.3
        Top7: BAD EYE
        Top8: Gcorr = 0.8
        Bot6: Gcorr = 1.4
        Bot7: BAD EYE
        Bot8: Gcorr = 1.5

        MMS3:
        Top6: Gcorr = 0.7
        Top7: Gcorr = 0.8
        Top8: Gcorr = 1.0
        Bot6: Gcorr = 0.9
        Bot7: Gcorr = 0.9
        Bot8: Gcorr = 1.3

        MMS4:
        Top6: Gcorr = 0.8
        Top7: BAD EYE
        Top8: Gcorr = 1.0
        Bot6: Gcorr = 0.8
        Bot7: Gcorr = 0.6
        Bot8: Gcorr = 0.9

'''

import pytplot
from pytplot import get_data, store_data

def mms_feeps_flat_field_corrections(probes = ['1', '2', '3', '4'], data_rate = 'brst', suffix = ''):
    G_corr = {}
    G_corr['mms1-top6'] = 0.7
    G_corr['mms1-top7'] = 2.5
    G_corr['mms1-top8'] = 1.5
    G_corr['mms1-bot5'] = 1.2 # updated 1/24
    G_corr['mms1-bot6'] = 0.9
    G_corr['mms1-bot7'] = 2.2 # updated 1/24
    G_corr['mms1-bot8'] = 1.0

    G_corr['mms2-top4'] = 1.2 # added 1/24
    G_corr['mms2-top6'] = 1.3
    G_corr['mms2-top7'] = 0 # bad eye
    G_corr['mms2-top8'] = 0.8
    G_corr['mms2-bot6'] = 1.4
    G_corr['mms2-bot7'] = 0 # bad eye
    G_corr['mms2-bot8'] = 1.5

    G_corr['mms3-top6'] = 0.7
    G_corr['mms3-top7'] = 0.8
    G_corr['mms3-top8'] = 1.0
    G_corr['mms3-bot6'] = 0.9
    G_corr['mms3-bot7'] = 0.9
    G_corr['mms3-bot8'] = 1.3

    G_corr['mms4-top6'] = 0.8
    G_corr['mms4-top7'] = 0 # bad eye
    G_corr['mms4-top8'] = 1.0
    G_corr['mms4-bot6'] = 0.8
    G_corr['mms4-bot7'] = 0.6
    G_corr['mms4-bot8'] = 0.9
    G_corr['mms4-bot9'] = 1.5 # added 1/24

    #sensor_ids = ['6', '7', '8']
    sensor_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    sensor_types = ['top', 'bottom']
    levels = ['l2']
    species = ['ion', 'electron']

    for probe in probes:
        for sensor_type in sensor_types:
            for sensor_id in sensor_ids:
                if G_corr.has_key('mms'+probes[probe_idx]+'-'+sensor_types[sensor_type][0:3]+sensor_ids[sensor_id]):
                    correction = G_corr['mms'+probes[probe_idx]+'-'+sensor_types[sensor_type][0:3]+sensor_ids[sensor_id]]
                else:
                    correction = 1.0

                for level in levels:
                    for species_id in species:
                        if correction != 1.0:
                            cr_var = 'mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+species_id+'_'+sensor_type+'_count_rate_sensorid_'+sensor_id+suffix
                            i_var = 'mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+species_id+'_'+sensor_type+'_intensity_sensorid_'+sensor_id+suffix
                            c_var = 'mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+species_id+'_'+sensor_type+'_counts_sensorid_'+sensor_id+suffix

                            cr_times, cr_data = get_data(cr_var)
                            i_times, i_data = get_data(i_var)
                            c_times, c_data = get_data(c_var)

                            cr_energies = pytplot.data_quants[cr_var].spec_bins.values
                            i_energies = pytplot.data_quants[i_var].spec_bins.values
                            c_energies = pytplot.data_quants[c_var].spec_bins.values

                            store_data(cr_var, data={'x': cr_times, 'y': cr_data*correction, 'v': cr_energies})
                            store_data(i_var, data={'x': i_times, 'y': i_data*correction, 'v': i_energies})
                            store_data(c_var, data={'x': c_times, 'y': c_data*correction, 'v': c_energies})




