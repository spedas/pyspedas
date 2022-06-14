
def spd_units_string(units, units_only=False):
    """
    Return string describing particle data units for labels

    Input:
        units: str
            String describing units

    Returns:
        String containing full units string
    """
    out = ['', 'Unknown', '']
    units = units.lower()

    if units == 'counts':
        out = ['', 'Counts', '']
    elif units == 'rate':
        out = ['Rate (', '#/sec', ')']
    elif units == 'eflux':
        out = ['Energy Flux (', 'eV / sec / cm² / ster / eV', ')']
    elif units == 'flux':
        out = ['Flux (', '# / sec / cm² / ster / eV', ')']
    elif units == 'df':
        out = ['f (', 's³ / cm³ / km³', ')']
    elif units == 'df_cm':
        out = ['f (', 's³ / cm⁶', ')']
    elif units == 'df_km':
        out = ['f (', 's³ / km⁶', ')']
    elif units == 'e2flux':
        out = ['Energy² Flux (', 'eV² / sec / cm² / ster /eV', ')']
    elif units == 'e3flux':
        out = ['Energy³ Flux (', 'eV³ / sec / cm² / ster /eV', ')']

    if units_only:
        return out[1]

    return ''.join(out)