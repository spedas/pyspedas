"""
;    To transform time series data from one coordinate to another. The supported coordinate 
;     systems are: SGA, SGI, DSI, J2000. Further transformation from J2000 to the 
;     geophysical coordinates (GEI, GSE, etc) can be processed by "cotrans()", which can be
      imported by (from pyspedas.cotrans_tools.cotrans import cotrans).
;     
;     The actual transformation is done by helper functions, such as sga2sgi(), sgi2dsi(), 
;     and dsi2j2000().
            
Main routine for coordinate transformation is erg_cotrans().
"""

from pyspedas import tcopy
from pytplot import tnames
from .dsi2j2000 import dsi2j2000
from .sga2sgi import sga2sgi
from .sgi2dsi import sgi2dsi


def erg_replace_coord_suffix(in_name=None, out_coord=None):
    nms = in_name.split('_')
    nms[-1] = out_coord
    return '_'.join(nms)


def erg_coord_trans(in_name=None,
                    out_name=None,
                    in_coord=None,
                    out_coord=None,
                    noload=False):

    if in_coord == out_coord:
        tcopy(in_name, out_name)
        return

    # From SGA
    if in_coord == 'sga':
        if out_coord == 'sgi':  # sga --> sgi
            sga2sgi(name_in=in_name, name_out=out_name, noload=noload)
        elif out_coord == 'dsi':  # sga --> sgi --> dsi
            name_sgi = erg_replace_coord_suffix(
                in_name=in_name, out_coord='sgi')
            sga2sgi(name_in=in_name, name_out=name_sgi, noload=noload)
            sgi2dsi(name_in=name_sgi, name_out=out_name, noload=noload)
        elif out_coord == 'j2000':  # sga --> sgi --> dsi --> j2000
            name_sgi = erg_replace_coord_suffix(
                in_name=in_name, out_coord='sgi')
            sga2sgi(name_in=in_name, name_out=name_sgi, noload=noload)
            name_dsi = erg_replace_coord_suffix(
                in_name=name_sgi, out_coord='dsi')
            sgi2dsi(name_in=name_sgi, name_out=name_dsi, noload=noload)
            dsi2j2000(name_in=name_dsi, name_out=out_name, noload=noload)

    # From SGI
    if in_coord == 'sgi':
        if out_coord == 'sga':  # sgi --> sga
            sga2sgi(name_in=in_name, name_out=out_name,
                    SGI2SGA=True, noload=noload)
        elif out_coord == 'dsi':  # sgi --> dsi
            sgi2dsi(name_in=in_name, name_out=out_name, noload=noload)
        elif out_coord == 'j2000':  # sgi --> dsi --> j2000
            name_dsi = erg_replace_coord_suffix(
                in_name=in_name, out_coord='dsi')
            sgi2dsi(name_in=in_name, name_out=name_dsi, noload=noload)
            dsi2j2000(name_in=name_dsi, name_out=out_name, noload=noload)

    # From DSI
    elif in_coord == 'dsi':

        if out_coord == 'sga':  # dsi --> sgi --> sga
            name_sgi = erg_replace_coord_suffix(
                in_name=in_name, out_coord='sgi')
            sgi2dsi(name_in=in_name, name_out=name_sgi,
                    DSI2SGI=True, noload=noload)
            sga2sgi(name_in=name_sgi, name_out=out_name,
                    SGI2SGA=True, noload=noload)
        elif out_coord == 'sgi':  # dsi --> sgi
            sgi2dsi(name_in=in_name, name_out=out_name,
                    DSI2SGI=True, noload=noload)
        elif out_coord == 'j2000':  # dsi --> j2000
            dsi2j2000(name_in=in_name, name_out=out_name, noload=noload)

    # From J2000
    elif in_coord == 'j2000':
        if out_coord == 'sga':  # j2000 --> dsi --> sgi --> sga
            name_dsi = erg_replace_coord_suffix(
                in_name=in_name, out_coord='dsi')
            dsi2j2000(name_in=in_name, name_out=name_dsi,
                      J20002DSI=True, noload=noload)
            name_sgi = erg_replace_coord_suffix(
                in_name=name_dsi, out_coord='sgi')
            sgi2dsi(name_in=name_dsi, name_out=name_sgi,
                    DSI2SGI=True, noload=noload)
            sga2sgi(name_in=name_sgi, name_out=out_name,
                    SGI2SGA=True, noload=noload)
        elif out_coord == 'sgi':  # j2000 --> dsi --> sgi
            name_dsi = erg_replace_coord_suffix(
                in_name=in_name, out_coord='dsi')
            dsi2j2000(name_in=in_name, name_out=name_dsi,
                      J20002DSI=True, noload=noload)
            sgi2dsi(name_in=name_dsi, name_out=out_name,
                    DSI2SGI=True, noload=noload)
        elif out_coord == 'dsi':  # j2000 --> dsi
            dsi2j2000(name_in=in_name, name_out=out_name,
                      J20002DSI=True, noload=noload)

# ;;;; Main routine for coordinate transformation ;;;;;


def erg_cotrans(in_name='',
                out_name='',
                in_coord='',
                out_coord='',
                noload=False):
    """
    Parameters:

        in_name : str
            name of input tplot variable to be transformed

        out_name : str
            Name of output tplot variable in which the transformed data are stored. 
            If not explicitly provided, out_name is automatically generated from
            "in_name" by replacing the coordinate name with a new one.
            For example, if you runs erg_cotrans(in_name='xxxx_sgi', out_coord='sga')
            then the result is stored in a newly created tplot variable 'xxxx_sga'.

        in_coord : str
            'sga', 'sgi', 'dsi', or 'j2000'
            Set to explicitly give the coordinate system name for the input variable.
            If not given, this routine tries to guess it from the name of the input
            tplot variable (in_name).

        out_coord : str
            'sga', 'sgi', 'dsi', or 'j2000'
            Set to explicitly give the coordinate system name for the output variable.
            If not given, the coordinate system name is obtained from the variable name
            as done for in_coord.

    Returns:
        None

    """
    valid_suffixes = ['sga', 'sgi', 'dsi', 'j2000']

    in_names = tnames(in_name)
    if len(in_names) == 0:
        print('in_name is not match in stored Tplot Variables, return')
        return

    for input_name in in_names:
        if in_coord not in valid_suffixes:
            if (input_name.split('_')[-1] in valid_suffixes):
                in_suf = input_name.split('_')[-1]
            else:
                print(
                    f'Cannot get a valid coord. suffix of input variable for {input_name}.')
                continue
        else:
            in_suf = in_coord
        if out_coord not in valid_suffixes:
            if out_name.split('_')[-1] in valid_suffixes:
                out_suf = out_name.split('_')[-1]
            else:
                print(
                    f'Cannot get a valid coord. suffix of output variable for {input_name}.')
                continue
        else:
            out_suf = out_coord
        if out_name == '':
            out_name_temp = erg_replace_coord_suffix(
                in_name=input_name, out_coord=out_suf)
            erg_coord_trans(in_name=input_name, out_name=out_name_temp,
                            in_coord=in_suf, out_coord=out_suf, noload=noload)
        else:
            erg_coord_trans(in_name=input_name, out_name=out_name,
                            in_coord=in_suf, out_coord=out_suf, noload=noload)
