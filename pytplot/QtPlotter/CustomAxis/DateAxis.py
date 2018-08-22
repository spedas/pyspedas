import pyqtgraph as pg
import time
import numpy as np

class DateAxis(pg.AxisItem):
    '''
    This class takes in tplot time variables and creates ticks/tick labels
    depending on the time length of the data.
    '''
    def tickStrings(self, values, scale, spacing):
        strns = []
        if values == []:
            return strns
        for x in values:
            try:
                rng = max(values)-min(values)
                print([time.strftime('%H:%M:%S',time.gmtime(i)) for i in values])
                # Less than four days' worth of data
                if rng < 3600*24*4:
                    # If a new day (some day at 00:00:00 UTC), go ahead and actually
                    # write out the date
                    if x % 86400 == 0:
                        # show YYYY-MM-DD
                        string = '%Y-%m-%d'
                        label1 = '%b %d -'
                        label2 = ' %b %d, %Y'
                    else:
                        # Just show hour and min.
                        string = '%H:%M'
                        label1 = '%b %d -'
                        label2 = ' %b %d, %Y'
                # Between four days' worth of data and ~ a month of data
                elif rng >= 3600*24*4 and rng < 3600*24*30:
                    # To keep things uncrowded, just putting month & day, and not the hour/min as well
                    string = '%m-%d'
                    label1 = '%b %d -'
                    label2 = ' %b %d, %Y'
                # Between ~ a months worth of data and two years' of worth of data
                elif rng >= 3600*24*30 and rng < 3600*24*30*24:
                    # Show abbreviated month name and full year (YYYY)
                    string = '%b-%Y'
                    label1 = '%Y -'
                    label2 = ' %Y'
                # Greater than two years' worth of data
                elif rng >=3600*24*30*24:
                    # Just show the year (YYYY)
                    string = '%Y'
                    label1 = ''
                    label2 = ''
                strns.append(time.strftime(string, time.gmtime(x)))
            except ValueError:
                # Windows can't handle dates before 1970
                strns.append(' ')
        try:
            label = time.strftime(label1, time.gmtime(min(values)))+time.strftime(label2, time.gmtime(max(values)))
        except ValueError:
            label = ''
        return strns

    def tickSpacing(self, minVal, maxVal, size):
        rng = maxVal - minVal
        if rng < 3600 * 24 * 4:
            # show ticks every four hours if you're looking at < four days of data
            levels = [(14400,0)]
            return levels
        elif rng >= 3600 * 24 * 4 and rng < 3600 * 24 * 30:
            # show ticks every two days if data between four days and ~ a month
            levels = [(172800,0)]
            return levels
        elif rng >= 3600 * 24 * 30 and rng < 3600 * 24 * 30 * 24:
            # show ticks ~ every month if data between ~ a month and ~ two years
            levels = [(2.592e+6,0)]
            return levels
        elif rng >= 3600 * 24 * 30 * 24:
            # show ticks ~ every year if data > two years
            # show ~ every year
            levels = [(3.154e+7,0)]
            return levels