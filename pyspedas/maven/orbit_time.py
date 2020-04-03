
"""
File:
    orbit_time.py

Description:
    MAVEN orbit file handling routines.
"""

import os


def month_to_num(month_string):

    month_to_num_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07',
                         'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}

    if month_string in month_to_num_dict.keys():
        return month_to_num_dict[month_string]
    else:
        raise ValueError('Month string is not valid')


def orbit_time(begin_orbit, end_orbit=None):
    orb_file = os.path.join(os.path.dirname(__file__),
                            'maven_orb_rec.orb')

    with open(orb_file, "r") as f:
        if end_orbit is None:
            end_orbit = begin_orbit
        orbit_num = []
        time = []
        f.readline()
        f.readline()
        for line in f:
            line = line[0:28]
            line = line.split(' ')
            line = [x for x in line if x != '']
            orbit_num.append(int(line[0]))
            time.append(line[1] + "-" + month_to_num(line[2]) + "-" + line[3] + "T" + line[4])
        try:

            if orbit_num.index(begin_orbit) > len(time) or orbit_num.index(end_orbit) + 1 > len(time):
                print("Orbit numbers not found.  Please choose a number between 1 and %s.", orbit_num[-1])
                return [None, None]
            else:
                begin_time = time[orbit_num.index(begin_orbit)]
                end_time = time[orbit_num.index(end_orbit) + 1]
        except ValueError:
            return [None, None]
    return [begin_time, end_time]
