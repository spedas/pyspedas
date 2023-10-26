from datetime import datetime
import numpy

def ave_spec(ts, cnts, periods):
    if isinstance(periods, tuple):
        periods = [periods]
    
    mask = False
    for (start, end) in periods:
        #convert start and end times to seconds since epoch
        epoch = datetime(1970, 1, 1)
        start_seconds = (datetime.strptime(start, "%Y-%m-%d/%H:%M") - epoch).total_seconds()
        end_seconds = (datetime.strptime(end, "%Y-%m-%d/%H:%M") - epoch).total_seconds()

        #add a section of valid timestamps to the boolean mask
        mask = mask | ((ts >= start_seconds) & (ts <= end_seconds))

    #use the mask to select just the counts that we are interested in and take their average
    selected = cnts[mask]
    return numpy.mean(selected, axis=0)

def average_event_spectrum(ts, cnts, nrg, bkg_periods, evt_periods):
    ave_bkg = ave_spec(ts, cnts, bkg_periods)
    ave_evt = ave_spec(ts, cnts, evt_periods)

    return ave_evt-ave_bkg

def background_subtracted_spectrogram(ts, cnts, nrg, bkg_periods):
    ave_bkg = ave_spec(ts, cnts, bkg_periods)
    
    return cnts-ave_bkg