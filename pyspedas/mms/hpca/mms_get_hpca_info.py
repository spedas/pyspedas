
def mms_get_hpca_info():
    """
    Returns structure containing hpca look directions, energies, and other info.

    """
     
    forward_anodes = [14,15,0,1,2,3,4,5]
    backward_anodes = [6,7,8,9,10,11,12,13]
    
    # approx spin period
    t_spin = 20.
    t_sweep = 0.625

    # anode elevation centroids in colat (indexed by anode #)
    elevation = [123.75,
                 101.25,
                 78.75,
                 56.25,
                 33.75,
                 11.25,
                 11.25,
                 33.75,
                 56.25,
                 78.75,
                 101.25,
                 123.75,
                 146.25,
                 168.75,
                 168.75,
                 146.25]

    # azimuth offsets for each energy within a sweep (indexed by energy bin #)
    # last step is not used for measurements
    azimuth_energy_offset = [0,
                             0.17,
                             0.341,
                             0.511,
                             0.681,
                             0.851,
                             1.021,
                             1.191,
                             1.361,
                             1.531,
                             1.701,
                             1.871,
                             2.042,
                             2.212,
                             2.382,
                             2.552,
                             2.722,
                             2.892,
                             3.062,
                             3.232,
                             3.402,
                             3.572,
                             3.743,
                             3.913,
                             4.083,
                             4.253,
                             4.423,
                             4.593,
                             4.763,
                             4.933,
                             5.103,
                             5.273,
                             5.444,
                             5.614,
                             5.784,
                             5.954,
                             6.124,
                             6.294,
                             6.464,
                             6.634,
                             6.804,
                             6.974,
                             7.145,
                             7.315,
                             7.485,
                             7.655,
                             7.825,
                             7.995,
                             8.165,
                             8.335,
                             8.505,
                             8.675,
                             8.846,
                             9.016,
                             9.187,
                             9.36,
                             9.535,
                             9.713,
                             9.894,
                             10.079,
                             10.269,
                             10.464,
                             10.666]
    
    return {'elevation': elevation, 't_spin': t_spin, 't_sweep': t_sweep, 'azimuth_energy_offset': azimuth_energy_offset}
