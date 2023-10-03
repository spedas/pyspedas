from datetime import datetime
import numpy

def bg_sub(ts, cnts, start, end):

    #convert start and end times to seconds since epoch
    epoch = datetime(1970, 1, 1)
    bkg_start_seconds = (datetime.strptime(start, "%Y-%m-%d/%H:%M") - epoch).total_seconds()
    bkg_end_seconds = (datetime.strptime(end, "%Y-%m-%d/%H:%M") - epoch).total_seconds()

    #create a boolean mask and apply it to the sspc data
    mask = (ts >= bkg_start_seconds) & (ts <= bkg_end_seconds)
    bkg_cnts = cnts[mask]
    times = ts[mask]

    bkg_spec = numpy.mean(bkg_cnts, axis=0)
    
    return cnts - bkg_spec