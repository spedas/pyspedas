# -*- coding: utf-8 -*-
"""
File:
    themis_helpers.py

Description:
    Helper functions for themis.
"""


def get_probes(probes):
    """Returns a list of probes"""
    probe_list = ['a', 'b', 'c', 'd', 'e']
    thprobe_list = ['tha', 'thb', 'thc', 'thd', 'the']
    ans_list = []
    if not isinstance(probes, (list, tuple)):
        probes = [probes]

    for p in probes:
        p = p.lower()
        if p == '*':
            ans_list = thprobe_list
            break
        if p in probe_list:
            ans_list.append('th' + p)
        elif p in thprobe_list:
            ans_list.append(p)

    return ans_list


def get_instruments(instruments, level):
    """Returns a list of themis instruments for L2 data"""
    if level == 'l1':
        instr_list = ['bau', 'eff', 'efp', 'efw', 'esa', 'fbk', 'fff_16',
                      'fff_32', 'fff_64', 'ffp_16', 'ffp_32', 'ffp_64',
                      'ffw_16', 'ffw_32', 'ffw_64', 'fgm', 'fit', 'hsk',
                      'mom', 'scf', 'scm', 'scmode', 'scp', 'scw', 'spin',
                      'sst', 'state', 'trg', 'vaf', 'vap', 'vaw']
    elif level == 'l2_mag':
        instr_list = instruments
    else:
        instr_list = ['efi', 'esa', 'fbk', 'fft', 'fgm', 'fit', 'gmom',
                      'mom', 'scm', 'sst']
    ans_list = []
    if not isinstance(instruments, (list, tuple)):
        instruments = [instruments]

    for p in instruments:
        p = p.lower()
        if p == '*':
            ans_list = instr_list
            break
        if p in instr_list:
            ans_list.append(p)

    return ans_list
