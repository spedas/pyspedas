import logging
from pyspedas.tplot_tools import get_units, get_coords, tkm2re, data_exists
from pyspedas.cotrans_tools.cotrans import cotrans

def pos_in_gsm(input_var: str,
               coord_in:str = None) -> str:
    """ Convert a position variable to GSM coordinates, if needed

    Parameters
    ----------
    input_var:str
        Name of the input tplot variable.
    coord_in: str
        (Optional) If set, specify the coordinate system of the input variable.  This overrides any coordinate
        system metadata that might be present.  Default: None Valid values: ["gse", "sm", "gsm", "gei", "geo", "mag", "j2000"]

    Returns
    -------
    string
        The name of a tplot variable guaranteed to be in GSM coordinates.  It may return
        the original variable if it was already in GSM, or a new variable that has been transformed.
    """

    if coord_in is None:
        coord_in = get_coords(input_var)
        if coord_in is None or coord_in == '':
            raise ValueError("pos_in_gsm: no coordinate system metadata available, cannot transform to GSM")
        if coord_in.lower() not in ["gse", "sm", "gsm", "gei", "geo", "mag", "j2000"]:
            raise ValueError(f"pos_in_gsm: unknown coordinate system {coord_in} in {input_var} metadata, cannot transform to GSM")
    elif coord_in.lower() in ["gse", "sm", "gsm", "gei", "geo", "mag", "j2000"]:
        # Are we overriding existing metadata?
        coord_var = get_coords(input_var)
        if coord_var is not None and coord_var != '':
            logging.warning(f"pos_in_gsm: Overriding existing coordinate metadata {coord_var} for variable {input_var}")
    else:
        raise ValueError(f"pos_in_gsm: unknown coord_in value {coord_in}, cannot transform to GSM")

    if coord_in.lower() == 'gsm':
        return input_var
    else:
        newname='input_var_gsm'
        cotrans(name_in=input_var, coord_in=coord_in, name_out=newname,coord_out='GSM')
        return newname

def pos_in_re(input_var:str,
                units_in:str = None) -> str:
    """ Convert a position variable to units of Re. if needed

    Parameters
    ----------
    input_var: str
        Name of the input tplot variable
    units_in: str
        (optional) Units of input tplot variable.  Overrides any units metadata that might be present. Default: None Valid values: ['km', 're']

    Returns
    -------
    str
    The name of a tplot variable guaranteed to be in units of Re.  May return original variable name if
    it was already in Re.
    """
    if units_in is None:
        units_in = get_units(input_var)
        if units_in is None or units_in == '':
            raise ValueError(f"pos_in_re: no units metadata available, unable to transform to Re")
        if units_in.lower() not in ['km', 're']:
            raise ValueError(f"pos_in_re: unknown unit {units_in} in {input_var} metadata, cannot transform to Re")
    elif units_in.lower() in ["km", "re"]:
        units_var = get_units(input_var)
        if units_var is not None and units_var != '':
            logging.warning(f"pos_in_re: Overriding existing units metadata {units_var} for variable {input_var}")

    else:
        raise ValueError(f"pos_in_re: unrecognized coord_in value {units_in}, cannot transform to Re")
    if units_in.lower() == 're':
        return input_var
    else:
        newname='input_var_re'
        tkm2re(input_var,newname=newname)
        return newname

def prepare_pos_variable(input_var:str,
                         units_in:str = None,
                         coord_in:str = None) -> str:
    """

    Parameters
    ----------
    input_var: str
    Name of the input tplot variable
    units_in: str
    (Optional) Units of input variable.  If specified, overrides any units metadata that might be present. Default: None  Valid values: ['km', 're']
    coord_in: str
    (Optional) Coordinate system of input variable.  If specified, overrides any coordinate system metadata that might be present. Default: None  Valid values: ["gse", "sm", "gsm", "gei", "geo", "mag", "j2000"]

    Returns
    -------
    str
    Variable name with input data transformed to GSM coordinates and units of Re.  May return original
    variable if no conversions are needed.
    """

    if not data_exists(input_var):
        raise ValueError(f"prepare_pos_variable: input variable {input_var} does not exist")
    input_re = pos_in_re(input_var, units_in=units_in)
    input_gsm_re = pos_in_gsm(input_re, coord_in = coord_in)
    return input_gsm_re
