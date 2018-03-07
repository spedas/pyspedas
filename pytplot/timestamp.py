from pytplot import extra_layouts
import datetime

def timestamp(val):  
    """
    This function will turn on a time stamp that shows up at the bottom of every generated plot.
    
    Parameters
        val  str
            A string that can either be 'on' or 'off'.  
            
    Returns
        None
    
    Examples
         # Turn on the timestamp
         import pytplot
         pytplot.timestamp('on')
    """
    
    
    
    if val is 'on':
        todaystring = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')
        extra_layouts['time_stamp'] = todaystring
    else:
        if 'time_stamp' in extra_layouts:
            del extra_layouts['time_stamp']
    
    return