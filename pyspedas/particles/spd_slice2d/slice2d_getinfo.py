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
            trange_str = ' -> '.join(time_string(the_slice['trange']))
        else:
            trange_str = ' -> '.join(the_slice['trange'])

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

        # add prefix
        if the_slice['energy']:
            xyprefix = 'E'
        else:
            xyprefix = 'V'

        if xtitle is None:
            xtitle = xyprefix + xt + ' (' + the_slice['xyunits'] + ')'

        if ytitle is None:
            ytitle = xyprefix + yt + ' (' + the_slice['xyunits'] + ')'

        if ztitle is None:
            ztitle = spd_units_string(the_slice['units_name'])

    return {'title': title, 'xtitle': xtitle, 'ytitle': ytitle, 'ztitle': ztitle}
