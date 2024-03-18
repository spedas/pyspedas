import logging
import pytplot


def tkm2re(name, km=False, newname=None, suffix=''):
    """
    Converts a tplot variable to Re or Km

    Parameters
    -----------
        name: str or list of str
            Names of tplot variables to convert

        km: bool, optional
            If True, convert Re to Km. If False, convert Km to Re.
            Default: False

        newname: str or list of str, optional
            Output variable names; if not set, the names of the
            input variables are used + '_re' or '_km'
            Default: None

        suffix: str, optional
            Specify to append a suffix to each variable 
            (only valid if newname is not specified)
            Default: ''

    Returns
    --------
        List of the tplot variables created

    Examples
    --------
        >>> import pytplot
        >>> pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> pytplot.tkm2re('a', km = True)
        >>> print(pytplot.data_quants['a_km'].data)

    """
    km_in_re = 6371.2

    names = pytplot.tnames(name)

    if names == []:
        logging.error('No tplot variables found: ' + name)
        return

    if newname is None:
        newname = [n + suffix for n in names]

        if km == False:
            newname = [n + '_re' for n in newname]
        else:
            newname = [n + '_km' for n in newname]
    else:
        if not isinstance(newname, list):
            newname = [newname]

        if len(newname) != len(names):
            logging.error('Number of output variable names (newname) should match the number of input variables.')
            return

    out = []

    for in_tvar, out_tvar in zip(names, newname):
        data = pytplot.get_data(in_tvar)
        metadata = pytplot.get_data(in_tvar, metadata=True)

        if data is None:
            logging.error('Problem reading variable: ' + in_tvar)
            continue

        if km == False:
            data_out = data.y/km_in_re
        else:
            data_out = data.y*km_in_re

        saved = pytplot.store_data(out_tvar, data={'x': data.times, 'y': data_out}, attr_dict=metadata)

        if not saved:
            logging.error('Problem creating tplot variable.')
            continue

        # update the subtitle, if needed
        yaxis_opt = pytplot.data_quants[out_tvar].attrs['plot_options'].get('yaxis_opt')

        if yaxis_opt is not None:
            subtitle = yaxis_opt.get('axis_subtitle')
            if subtitle is not None:
                if km == False:
                    new_subtitle = pytplot.data_quants[out_tvar].attrs['plot_options']['yaxis_opt']['axis_subtitle'].lower().replace('km', 'Re')
                else:
                    new_subtitle = pytplot.data_quants[out_tvar].attrs['plot_options']['yaxis_opt']['axis_subtitle'].lower().replace('re', 'km')
                pytplot.data_quants[out_tvar].attrs['plot_options']['yaxis_opt']['axis_subtitle'] = new_subtitle

        out.append(out_tvar)

    return out
