
def erg_units_string(units, units_only=False,simple=False,relativistic=False):
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

    if simple:
        if units == 'counts':
            out = ['', 'Counts', '']
        elif units == 'rate':
            out = ['Rate (','#/sec',')']
        elif units == 'eflux':
            out = ['Energy Flux (','eV / sec / cm^2 / ster / eV',')']
        elif units == 'flux':
            out = ['Flux (','# / sec / cm^2 / ster / eV',')']
        elif units == 'df':
            if relativistic:
                out = ['PSD (', '(c/MeV/cm)^3', ')']
            else:
                out = ['PSD (', 's^3 / km^6', ')']
        elif units == 'psd':
            if relativistic:
                out = ['PSD (', '(c/MeV/cm)^3', ')']
            else:
                out = ['PSD (', 's^3 / km^6', ')']
        elif units == 'df_cm':
            out = ['PSD (','s^3 / cm^6',')']
        elif units == 'df_km':
            out = ['PSD (','s^3 / km^6',')']
        elif units == 'e2flux':
            out = ['Energy^2 Flux (','eV^2 / sec / cm^2 / ster /eV',')']
        elif units == 'e3flux':
            out = ['Energy^3 Flux (','eV^3 / sec / cm^2 / ster /eV',')']
    else:
        if units == 'counts':
            out = ['','Counts','']
        elif units == 'rate':
            out = ['Rate (','#/sec',')']
        elif units == 'eflux':
            out = ['Energy Flux (','eV/s/'+'$cm^{2}$'+'/str/eV',')']
        elif units == 'flux':
            out = ['Flux (','#/s/'+'$cm^{2}$'+'/str/eV',')']
        elif units == 'df':
            if relativistic:
                out = ['Phase space density (', '(c/MeV/cm)'+'$^{3}$', ')']
            else:
                out = ['Phase space density (', 's'+'$^{3}$'+'/km'+'$^{6}$', ')']
        elif units == 'psd':
            if relativistic:
                out = ['Phase space density (', '(c/MeV/cm)'+'$^{3}$', ')']
            else:
                out = ['Phase space density (', 's'+'$^{3}$'+'/km'+'$^{6}$', ')']
        elif units == 'df_cm':
            out = ['Phase space density (','s'+'$^{3}$'+'/cm'+'$^{6}$',')']
        elif units == 'df_km':
            out = ['Phase space density (','s'+'$^{3}$'+'/km'+'$^{6}$',')']
        elif units == 'e2flux':
            out = ['Energy$^{2}$ Flux (','eV'+'$^{2}$'+'/s/cm'+'$^{2}$'+'/str/eV',')']
        elif units == 'e3flux':
            out = ['Energy$^{3}$ Flux (','eV'+'$^{3}$'+'/s/cm'+'$^{2}$'+'/str/eV',')']

    if units_only:
        return out[1]

    return ''.join(out)