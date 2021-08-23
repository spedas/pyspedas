
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
        out = ['Energy Flux (', 'eV / sec / cm^2 / ster / eV', ')']
    elif units == 'flux':
        out = ['Flux (', '# / sec / cm^2 / ster / eV', ')']
    elif units == 'df':
        out = ['f (', 's^3 / cm^3 / km^3', ')']
    elif units == 'df_cm':
        out = ['f (', 's^3 / cm^6', ')']
    elif units == 'df_km':
        out = ['f (', 's^3 / km^6', ')']
    elif units == 'e2flux':
        out = ['Energy^2 Flux (', 'eV^2 / sec / cm^2 / ster /eV', ')']
    elif units == 'e3flux':
        out = ['Energy^3 Flux (', 'eV^3 / sec / cm^2 / ster /eV', ')']

    if units_only:
        return out[1]

    return ''.join(out)