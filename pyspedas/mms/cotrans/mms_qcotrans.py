import logging
from pyspedas import cotrans_get_coord
from pytplot import get_data
from .mms_cotrans_qtransformer import mms_cotrans_qtransformer

try:
    import spacepy.coordinates as coord
except ImportError:
    logging.error('SpacePy must be installed to use this module.')
    logging.error('Please install it using: pip install spacepy')


def mms_qcotrans(in_name=None, out_name=None, in_coord=None, out_coord=None, probe=None):
    """
    Perform coordinate transformations using MMS MEC quaternions.

    This routine uses SpacePy to do the quaternion transformation operations.

    Parameters
    -----------
        in_name: str or list of str
            Names of Tplot variables of vectors to be transformed

        out_name: str or list of str
            Names of output variables

        in_coord: str
            Input coordinate system (e.g. 'bcs','gse','gse2000','gsm','sm','geo','eci')

        out_coord: str
            Output coordinate system (e.g. 'bcs','gse','gse2000','gsm','sm','geo','eci')

        probe: str
            MMS spacecraft # (must be 1, 2, 3, or 4)

    Returns
    --------
        List of variables created

    """
    valid_probes = ['1', '2', '3', '4']
    valid_coords = ['bcs', 'dbcs', 'dmpa', 'smpa', 'dsl', 'ssl', 'gse', 'gse2000', 'gsm', 'sm', 'geo', 'eci', 'j2000']

    if in_name is None:
        logging.error('Input variable name is missing')
        return

    if out_name is None:
        logging.error('Output variable name is missing')
        return

    if not isinstance(in_name, list):
        in_name = [in_name]

    if not isinstance(out_name, list):
        out_name = [out_name]

    out_vars = []

    for idx, variable in enumerate(in_name):
        if in_coord is None:
            var_coords = cotrans_get_coord(variable)
            in_coord = var_coords
            if var_coords is None:
                logging.error('Could not determine coordinate system for: ' + variable)
                continue

        if isinstance(in_coord, list):
            var_coords = in_coord[idx]
        else:
            var_coords = in_coord

        var_coords = var_coords.lower()

        if var_coords not in valid_coords:
            logging.error('Unsupported input coordinate system: ' + var_coords)
            continue

        if isinstance(out_coord, list):
            new_coords = out_coord[idx]
        else:
            new_coords = out_coord

        new_coords = new_coords.lower()

        if new_coords not in valid_coords:
            logging.error('Unsupported output coordinate system: ' + new_coords)

        if var_coords in ['bcs', 'ssl'] or new_coords in ['bcs', 'ssl']:
            logging.warning('WARNING: there are issues transforming data to/from a spinning coordinate system')

        # find the probe, if it's not specified by the user
        if probe is None:
            name_pieces = variable.split('_')
            if len(name_pieces) <= 1:
                logging.warning('Probe could not be determined from: ' + variable + '; defaulting to probe 1')
                probe = '1'
            else:
                probe = name_pieces[0][-1]

        if not isinstance(probe, str):
            probe = str(probe)

        if probe not in valid_probes:
            logging.error('Unknown probe for variable: ' + variable + '; continuing without transforming...')
            continue

        transformed = mms_cotrans_qtransformer(variable, out_name[idx], var_coords, new_coords, probe=probe)

        if transformed is not None:
            out_vars.append(transformed)

            # update the coordinate system in the plot metadata if needed
            metadata = get_data(transformed, metadata=True)
            if metadata.get('plot_options') is not None:
                if metadata['plot_options'].get('yaxis_opt') is not None:
                    if metadata['plot_options']['yaxis_opt'].get('legend_names') is not None:
                        legend = metadata['plot_options']['yaxis_opt'].get('legend_names')
                        updated_legend = [item.replace(var_coords.upper(), new_coords.upper()) for item in legend]
                        metadata['plot_options']['yaxis_opt']['legend_names'] = updated_legend
                    if metadata['plot_options']['yaxis_opt'].get('axis_label') is not None:
                        ytitle = metadata['plot_options']['yaxis_opt'].get('axis_label')
                        metadata['plot_options']['yaxis_opt']['axis_label'] = ytitle.replace(var_coords.upper(),
                                                                                             new_coords.upper())
    return out_vars
