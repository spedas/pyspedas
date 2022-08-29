from pyspedas import time_string
from pyspedas.particles.spd_units_string import spd_units_string


def slice2d_getinfo(the_slice, title=None, xtitle=None, ytitle=None, ztitle=None):
    """
    Forms various title annotations based on the slice's metadata
    """
    if title is None:
        sc = the_slice.get('spacecraft')
        if sc is None:
            sc = ''

        if not isinstance(the_slice['trange'][0], str):
            trange_str = ' -> '.join(time_string(the_slice['trange'])) + ' (' + str(the_slice['n_samples']) + ')'
        else:
            trange_str = ' -> '.join(the_slice['trange']) + ' (' + str(the_slice['n_samples']) + ')'

        title = the_slice['project_name'] + ' ' + sc + ' ' + the_slice['data_name'] + ' (' + the_slice[
            'rotation'] + ') ' + trange_str

    if xtitle is None or ytitle is None:
        xt = 'x'
        yt = 'y'

        rot = the_slice['rotation']

        if rot == 'yz':
            xt = 'y'
            yt = 'z'
        elif rot == 'xz':
            xt = 'x'
            yt = 'z'
        elif rot == 'bv':
            xt = 'B'
            yt = 'V'
        elif rot == 'be':
            xt = 'B'
            yt = 'B x V'
        elif rot == 'xvel':
            xt = 'x'
            yt = 'V'
        elif rot == 'perp':
            xt = 'V perp B'
            yt = 'B x V'
        elif rot == 'perp_xy':
            xt = '$x_{perp}$'
            yt = '$y_{perp}$'
        elif rot == 'perp_xz':
            xt = '$x_{perp}$'
            yt = '$z_{perp}$'
        elif rot == 'perp_yz':
            xt = '$y_{perp}$'
            yt = '$z_{perp}$'
        elif rot == 'b_exb':
            xt = 'B'
            yt = 'V perp B'
        elif rot == 'perp1-perp2':
            xt = 'B x V'
            yt = 'V perp B'

        # add prefix
        if the_slice['energy']:
            xyprefix = 'E'
        else:
            xyprefix = 'V'

        if the_slice['rlog']:
            xyprefix = 'log(' + xyprefix + ')'

        if xtitle is None:
            if rot not in ['perp_xy', 'perp_xz', 'perp_yz']:
                xtitle = '$' + xyprefix + '_{' + xt + '}$ (' + the_slice['xyunits'] + ')'
            else:
                xtitle = xyprefix + xt + ' (' + the_slice['xyunits'] + ')'

        if ytitle is None:
            if rot not in ['perp_xy', 'perp_xz', 'perp_yz']:
                ytitle = '$' + xyprefix + '_{' + yt + '}$ (' + the_slice['xyunits'] + ')'
            else:
                ytitle = xyprefix + yt + ' (' + the_slice['xyunits'] + ')'

        if ztitle is None:
            ztitle = spd_units_string(the_slice['units_name'])

    return {'title': title, 'xtitle': xtitle, 'ytitle': ytitle, 'ztitle': ztitle}
