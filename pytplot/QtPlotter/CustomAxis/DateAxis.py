import pyqtgraph as pg
import time


class DateAxis(pg.AxisItem):
    """
    This class takes in tplot time variables and creates ticks/tick labels
    depending on the time length of the data.
    """
    def tickStrings(self, values, scale, spacing):
        strns = []
        if not values:
            return strns
        for x in values:
            try:
                rng = max(values)-min(values)
                # Less than five minutes' worth of data
                if rng < 300:
                    # Show hour, min, and sec.
                    string = '%H:%M:%S'
                    label1 = '%b %d -'
                    label2 = ' %b %d, %Y'
                # Between five minutes' and four days' worth of data
                elif 300 <= rng < 3600*24*4:
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
                elif 3600*24*4 <= rng < 3600*24*30:
                    # To keep things uncrowded, just putting month & day, and not the hour/min as well
                    string = '%m-%d'
                    label1 = '%b %d -'
                    label2 = ' %b %d, %Y'
                # Between ~ a months worth of data and two years' of worth of data
                elif 3600*24*30 <= rng < 3600*24*30*24:
                    # Show abbreviated month name and full year (YYYY)
                    string = '%b-%Y'
                    label1 = '%Y -'
                    label2 = ' %Y'
                # Greater than two years' worth of data
                elif rng >= 3600*24*30*24:
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
        if rng < 4:
            # Show ticks every second if you're looking at < four seconds' worth of data
            levels = [(1, 0)]
            return levels
        elif 4 <= rng < 15:
            # Show ticks every two seconds if you're looking between four and 15 seconds' worth of data
            levels = [(2, 0)]
            return levels
        elif 15 <= rng < 60:
            # Show ticks every five seconds if you're looking between 15 seconds' and one minutes' worth of data
            levels = [(5, 0)]
            return levels
        elif 60 <= rng < 300:
            # Show ticks every 30 seconds if you're looking between 1 and 5 minutes worth of data
            levels = [(30, 0)]
            return levels
        elif 300 <= rng < 600:
            # Show ticks every minute if you're looking between 5 and 10 minutes worth of data
            levels = [(60, 0)]
            return levels
        elif 600 <= rng < 1800:
            # Show ticks every 5 minutes if you're looking between 10 and 30 minutes worth of data
            levels = [(300, 0)]
            return levels
        elif 1800 <= rng < 3600:
            # Show ticks every 15 minutes if you're looking between 30 minutes' and one hours' worth of data
            levels = [(900, 0)]
            return levels
        elif 3600 <= rng < 3600*2:
            # Show ticks every 30 minutes if you're looking between one and two hours' worth of data
            levels = [(1800, 0)]
            return levels
        elif 3600*2 <= rng < 3600*6:
            # Show ticks every hour if you're looking between two and six hours' worth of data
            levels = [(3600, 0)]
            return levels
        elif 3600*6 <= rng < 3600*12:
            # Show ticks every two hours if you're looking between six and 12 hours' worth of data
            levels = [(7200, 0)]
            return levels
        elif 3600*12 <= rng < 3600*24:
            # Show ticks every four hours if you're looking between 12 hours' and one days' worth of data
            levels = [(14400, 0)]
            return levels
        elif 3600*24 <= rng < 3600*24*2:
            # Show ticks every six hours if you're looking at between one and two days' worth of data
            levels = [(21600, 0)]
            return levels
        elif 3600*24*2 <= rng < 3600*24*4:
            # show ticks every 12 hours if you're looking between two and four days' worth of data
            levels = [(43200, 0)]
            return levels
        elif 3600*24*4 <= rng < 3600*24*30:
            # show ticks every two days if data between four days and ~ a month
            levels = [(172800, 0)]
            return levels
        elif 3600*24*30 <= rng < 3600*24*30*24:
            # show ticks ~ every month if data between ~ a month and ~ two years
            levels = [(2.592e+6, 0)]
            return levels
        elif rng >= 3600*24*30*24:
            # show ticks ~ every year if data > two years
            # show ~ every year
            levels = [(3.154e+7, 0)]
            return levels
