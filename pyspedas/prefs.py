# -*- coding: utf-8 -*-
"""
File:
    prefs.py

Desrciption:
    Loads preferences.
"""

import os


def get_prefs_filename():

    dir_path = os.path.abspath(os.path.dirname(__file__))
    fname = os.path.join(dir_path, 'spd_prefs_txt.py')

    print(fname)

    return fname


def get_spedas_prefs():
    """Get all the spedas preferences and return a directory"""

    fname = get_prefs_filename()
    print("Preferences file: " + fname)

    """Read preferences"""
    with open(fname, 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    """Fill dictionary"""
    ans_dict = {}
    for line in content:
        if len(line) > 2 and line[0] != "#":
            terms = line.split('=')
            terms = [x.strip() for x in terms]
            if len(terms) == 2:
                if terms[0] != '' and terms[1] != '':
                    ans_dict[terms[0].replace("'", "")] = terms[1].replace("'",
                                                                           "")

    f.closed
    return ans_dict


def set_spedas_prefs(var_name, var_value):
    """Get all the spedas preferences and return a directory"""

    found = 0
    if var_name == '' or var_value == '':
        return found

    fname = get_prefs_filename()
    print("Preferences file: " + fname)

    """Read preferences"""
    with open(fname, 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    """Make change"""
    new_content = ''
    for line in content:
        new_line = line
        if len(line) > 2 and line[0] != "#":
            terms = line.split('=')
            terms = [x.strip() for x in terms]
            if len(terms) == 2:
                if terms[0] != '' and terms[1] != '':
                    if terms[0] == var_name:
                        new_line = var_name + "='" + var_value + "'"
                        found = 1
        new_line = new_line.replace(os.linesep, '\n').strip()
        if new_line != '':
            new_content += new_line + '\n'

    with open(fname, 'w') as f:
        f.write(new_content)
    f.closed

    return found
