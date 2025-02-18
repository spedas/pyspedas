import numpy as np
import logging
from .lingradest import lingradest
from pyspedas import tinterpol
from pytplot import (get_data, store_data, time_double, time_string, time_clip, deflag, tnames,
                     options, tplot_options, tsmooth, tplot, get_coords, get_units, set_coords, set_units)

def classify_null_type(lambdas_in):
    """
    Determine the topological type of a magnetic null, given the eigenvalues of the Jacobian matrix.

    Parameters
    ----------
    lambdas_in: An array of 3 complex-valued eigenvalues of the Jacobian matrix,
        in no particular order.

    Returns
    -------
    int
        An integer representing the null type::

       0: Unknown/unable to characterize
       1: X-type null
       2: O-type null (island or plasmoid)
       3: A-type (radial) null
       4: B-type (radial) null
       5: A_s-type (spiral) null
       6: B_s-type (spiral) null
       7: X-type, degenerated from A type
       8: X-type, degenerated from B type
       9: O-type, degenerated from A_s type
       10: O-type, degenerated from B_s type

    See Table 1, Fu et al 2015 for details

    References
    ----------
    Fu, H. S., A. Vaivads, Y. V. Khotyaintsev, V. Olshevsky, M. André, J. B. Cao, S. Y. Huang,
    A. Retinò, and G. Lapenta (2015), How to find magnetic nulls and reconstruct field topology
    with MMS data?. J. Geophys. Res. Space Physics, 120, 3758–3782. doi: 10.1002/2015JA021082.

    Paschmann, G., Daly, P. (1998), Analysis Methods for Multi-Spacecraft Data, ISSR
    """

    lambda1 = lambdas_in[0]
    lambda2 = lambdas_in[1]
    lambda3 = lambdas_in[2]

    # We want to find the max and min (absolute value) norms, real, and imaginary parts,
    # to decide later if 3-d type nulls should degenerate to 2-d type nulls

    n1 = np.abs(lambda1)
    n2 = np.abs(lambda2)
    n3 = np.abs(lambda3)
    nlist = np.array([n1,n3,n3])
    n_max = np.max(nlist)
    n_min = np.min(nlist)

    re1 = np.abs(lambda1.real)
    re2 = np.abs(lambda2.real)
    re3 = np.abs(lambda2.real)
    re_list = np.array([re1,re2,re3])
    re_max = np.max(re_list)
    re_min = np.min(re_list)

    im1 = np.abs(lambda1.imag)
    im2 = np.abs(lambda2.imag)
    im3 = np.abs(lambda3.imag)
    # One of the eigenvalues is always pure real. So for this comparison, we only want to
    # consider the ones that might have imaginary components.  If they're all real, it won't matter.
    if (im1 == 0.0):
        im_list = np.array([im2,im3])
    elif (im2 == 0.0):
        im_list = np.array([im1,im3])
    else:
        im_list = np.array([im1,im2])
    im_max = np.max(im_list)
    im_min = np.min(im_list)


    # Now we order by size of the norms
    if (n1 <= n2) and (n2 <= n3):
        s1 = lambda1
        s2 = lambda2
        s3 = lambda3
    elif (n1 <= n3) and (n3 <= n2):
        s1 = lambda1
        s2 = lambda3
        s3 = lambda2
    elif (n2 <= n3) and (n3 <= n1):
        s1 = lambda2
        s2 = lambda3
        s3 = lambda1
    elif (n2 <= n1) and (n1 <= n3):
        s1 = lambda2
        s2 = lambda1
        s3 = lambda3
    elif (n3 <= n1) and (n1 <= n2):
        s1 = lambda3
        s2 = lambda1
        s3 = lambda2
    else:
        s1 = lambda3
        s2 = lambda2
        s3 = lambda1

    typecode = 0  # Default to unclassified

    # Now we can classify the null type.  It should be safe to use floating point equality to check
    # the imaginary parts.  It is unlikely that any of the real parts or norms will be exactly 0,
    # but see below where we check for some possibly degenerate cases.

    # Note: this logic appears to classify everything, with no "unknown" type nulls.  But in
    # Hu's paper, unknown type seems to happen fairly frequently. I suspect some of my typecode 5 and
    # 6 classifications might become "unknown" if I also looked at the components of the complex eigenvalues,
    # rather than just checking the sign of the pure real.

    if (s1.imag == 0.0) and (s2.imag == 0.0) and (s3.imag == 0.0):  # all eigenvalues pure real
        if (s1.real == 0.0):  # smallest (absolute val) real is exactly 0
            typecode = 1 # type X
        elif (s3.real > 0.0): # largest (absolute val) real part is +ve
            typecode = 3 # type A
        else: # largest (abs) real part is -ve
            typecode = 4  # type B
    elif (n1 == 0.0): # one pure real == 0, other two imaginary
        typecode = 2 # O-type
    else:  # all eigenvalues nonzero, one pure real two imaginary
        if (s1.imag == 0.0): # s1 is the pure real eigenvalue
            if s1.real > 0.0:   # real eigenvalue is +ve
                typecode = 5 # A_s
            else:               # real eigenvalue is -ve
                typecode = 6 # B_s
        elif (s2.imag == 0.0): # s2 is the pure real eigenvalue
            if s2.real > 0.0:   # real eigenvalue is +ve
                typecode = 5 # A_s
            else:               # real eigenvalue is -ve
                typecode = 6 # B_s
        else:   # s3 must be the pure real
            if s3.real > 0.0:
                typecode = 5 # A_s
            else:
                typecode = 6 # B_s


    # Now check to see if a 3-d null should degenerate to a 2-d type of null
    # Type A and B nulls should degenerate to type X if min(norms) < .25*max(norms)
    # Type A_s and B_s nulls should degenerate to type O if max(real) < 0.25*min(imag)

    if (typecode == 3) or (typecode == 4): # Type A or B
        if n_min < 0.25 * n_max:
            typecode = typecode + 4 # degenerate to X-type
    elif (typecode == 5) or (typecode == 6):  # Type A_s or B_s
        if re_max < 0.25*im_min:
            typecode = typecode + 4   # degenerate to O-type
    return typecode


# Define some stuff we'll use in debugging messages and plot options

typecode_strings = ['Unknown','X','O','A','B','A_s', 'B_s','X_a','X_b','O_a','O_b']
typecode_symbols = ['.','x','$o$','4','4','>','>','x','x','$o$','$o$']
typecode_colors = ['k','k','k','r','b','r','b','r','b','r','b']

def find_magnetic_nulls_fote(positions=None, fields=None, smooth_fields=True, smooth_npts=10, smooth_median=True,scale_factor=1.0):
    """
    Find magnetic null points, using the First Order Taylor Expansion (FOTE) method, from a set of four-point magnetic field observations.

    Parameters
    -----------

    positions: list of str
        A 4-element list of tplot variable names representing the probe positions

    fields: list of str
        A 4-element list of tplot variable names representing the magnetic field measurements

    smooth_fields: bool
        If True, perform boxcar averaging on the fields
        Default: True

    smooth_npts: int
        Number of points to use in the boxcar smoothing, if smoothing is enabled.

    smooth_median: bool
        If True and smoothing is enabled, use median filtering
        Default: True

    scale_factor: float
        The scale factor passed to the lingradest routine to scale some of the distances
        Default: 1.0

    Returns
    -------
    list of str
        A list of tplot variables describing the nulls found::

            'null_pos': Position of the null point, in the same coordinate system as imput positions
            'null_bary_dist': Distance between the null point and the barycenter of the tetrahedron
            'null_bary_dist_types': A composite variable more suitable for plotting, with the null to barycenter distances,
                  superimposed with symbols representing the type of each null found
            'null_sc_distances': The distances from the null to each of the four spacecraft
            'null_fom': Figures of merit 'eta' and 'xi', roughly representing the confidence in the null location and null type.
                  Lower is better, with values less than 0.4 denoting fairly reliable detection and classification
            'null_typecode': The type of each null point found, with values from 0-6. See classify_null_type() for interpretation.
            'max_reconstruction_error': The maximum error out of the four s/c, when using the calculated Jacobian and field
                  at the barycenter to reconstruct the field vectors at each spacecraft.  Should be extremely close to zero.


    Notes
    ------

    This routine uses tetrahedral interpolation to estimate the magnetic field (B0) and field gradients at the tetrahedron
    barycenter. From the field gradients we can construct a Jacobian matrix (J).  The field in that region can be
    expressed, to a first order approximation, as

    B = B0 + JV

    where V is the position vector relative to the barycenter.  At a magnetic null V_null, all components of B are zero,
    so we have JV_null = -B0, which can be solved to get V_null.

    As long as the four field measurements all differ, a null point will always be found.   For it to be credible,
    it should be in the neighborhood where the linear gradient approximation is expected to be valid, i.e. some smallish multiple
    of the tetrahedron size.

    The topology of the field around the null can be inferred from the eigenvalues and eigenvectors of the
    estimated Jacobian. See the classify_null_type() function for details.

    References
    -----------

    Fu, H. S., A. Vaivads, Y. V. Khotyaintsev, V. Olshevsky, M. André, J. B. Cao, S. Y. Huang,
    A. Retinò, and G. Lapenta (2015), How to find magnetic nulls and reconstruct field topology
    with MMS data?. J. Geophys. Res. Space Physics, 120, 3758–3782. doi: 10.1002/2015JA021082.

    Paschmann, G., Daly, P. (1998), Analysis Methods for Multi-Spacecraft Data, ISSR


    Example
    -------

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> data = pyspedas.projects.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-09-19/07:40', '2015-09-19/07:45'], data_rate='srvy', time_clip=True, varformat='*_gse_*', get_fgm_ephemeris=True)
    >>> fields = ['mms'+prb+'_fgm_b_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
    >>> positions = ['mms'+prb+'_fgm_r_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
    >>> null_vars = pyspedas.find_magnetic_nulls_fote(fields=fields, positions=positions, smooth_fields=True,smooth_npts=10,smooth_median=True)
    >>> tplot(null_vars)
    """

    # Input data needs to be sanitized, by removing any nans, and finding a time range common
    # to all the deflagged variables

    positions_df = []
    fields_df = []
    fields_sm = []

    for i in range(4):
        positions_df.append(positions[i]+'_df')
        fields_df.append(fields[i]+'_df')
        if smooth_fields:
            fields_sm.append(fields[i]+'_sm')
        else:
            fields_sm.append(fields[i]+'_df')

        deflag(positions[i], method='remove_nan', newname=positions_df[i])
        deflag(fields[i], method='remove_nan', newname=fields_df[i])
        if smooth_fields:
            tsmooth(fields_df[i], width=smooth_npts, median=smooth_median, newname=fields_sm[i])

    # Interpolate all deflagged positions and field measurements to the first probe's field measurement times

    # We need to find a time range that's contained in all the position and field variables, to
    # prevent interpolation from introducing NaNs and causing exceptions to be thrown in the calculations
    # below.

    tmin = 0.0
    tmax = time_double('3000-01-01')
    for i in range(4):
        d = get_data(positions_df[i])
        dmin = d.times[0]
        dmax = d.times[-1]
        tmin = np.max([tmin, dmin])
        tmax = np.min([tmax, dmax])

        d = get_data(fields_sm[i])
        dmin = d.times[0]
        dmax = d.times[-1]
        tmin = np.max([tmin, dmin])
        tmax = np.min([tmax, dmax])

    # Shave another millisecond off each end just to be sure (because floating point equality testing is weird)
    tmin = tmin + .001
    tmax = tmax - .001

    # We'll interpolate everything to the first set of times, so we'll time_clip that one to the desired time range
    time_clip(fields_sm[0], tmin, tmax, newname='f0_tc')

    # Now we can interpolate safely
    tinterpol(positions_df,'f0_tc',newname=['pos1_i','pos2_i','pos3_i','pos4_i'])
    tinterpol(fields_sm, 'f0_tc', newname=['b1_i','b2_i','b3_i','b4_i'])

    # Get the data arrays from the interpolated tplot variables
    d1 = get_data('pos1_i')
    d2 = get_data('pos2_i')
    d3 = get_data('pos3_i')
    d4 = get_data('pos4_i')

    # Position variables for MMS include a total distance as the last element, so only take the first three
    r1=d1.y[:,0:3]
    r2=d2.y[:,0:3]
    r3=d3.y[:,0:3]
    r4=d4.y[:,0:3]

    b1 = get_data('b1_i')
    b2 = get_data('b2_i')
    b3 = get_data('b3_i')
    b4 = get_data('b4_i')

    # The MMS field variables also include a fourth component with the total field
    bx1 = b1.y[:,0]
    by1 = b1.y[:,1]
    bz1 = b1.y[:,2]

    bx2 = b2.y[:,0]
    by2 = b2.y[:,1]
    bz2 = b2.y[:,2]

    bx3 = b3.y[:,0]
    by3 = b3.y[:,1]
    bz3 = b3.y[:,2]

    bx4 = b4.y[:,0]
    by4 = b4.y[:,1]
    bz4 = b4.y[:,2]

    datapoint_count = len(bx1)
    times = b1.times


    # Call the lingradest routine to get the barycenter locations, field at barycenter, and field gradients at barycenter

    # Output of lingradest is a dictionary of string keys and numpy array values

    lingrad_output = lingradest(bx1, bx2, bx3, bx4,
                                by1, by2, by3, by4,
                                bz1, bz2, bz3, bz4,
                                r1,r2,r3,r4, scale_factor=scale_factor)

    # Output arrays
    out_pos_null = np.zeros((datapoint_count,3))
    out_pos_bary = np.zeros((datapoint_count,3))
    out_null_bary_dist = np.zeros((datapoint_count))
    out_null_p1_dist = np.zeros((datapoint_count))
    out_null_p2_dist = np.zeros((datapoint_count))
    out_null_p3_dist = np.zeros((datapoint_count))
    out_null_p4_dist = np.zeros((datapoint_count))
    out_null_eta = np.zeros((datapoint_count))
    out_null_xi = np.zeros((datapoint_count))
    out_typecode = np.zeros((datapoint_count))
    out_max_reconstruction_error = np.zeros((datapoint_count))

    for i in range(datapoint_count):
        Rbary = lingrad_output['Rbary'][i]
        out_pos_bary[i,:] = Rbary[:]

        # Get field vector at barycenter for i-th point
        bxbc = lingrad_output['Bxbc'][i]
        bybc = lingrad_output['Bybc'][i]
        bzbc = lingrad_output['Bzbc'][i]
        b0 = np.array((bxbc, bybc, bzbc)) # Field at barycenter
        b0_neg = np.array((-bxbc,-bybc,-bzbc))  # Negative of field at barycenter

        # Form Jacobian matrix from field gradients at barycenter
        LGBx = lingrad_output['LGBx'][i]
        LGBy = lingrad_output['LGBy'][i]
        LGBz = lingrad_output['LGBz'][i]
        J = np.stack((LGBx, LGBy, LGBz))  # Jacobian matrix

        # Solve for null position with respect to barycenter (maybe check for singular matrix first?)

        r_null = np.linalg.solve(J,b0_neg)
        F_null = b0 + np.matmul(J,r_null)
        r_null_bary_dist = np.linalg.norm(r_null)
        out_null_bary_dist[i] = r_null_bary_dist

        # Translate r_null to origin of probe coordinate system
        pos_null = r_null + Rbary
        out_pos_null[i,:] = pos_null[:]

        # Get distances from null to each probe in the tetrahedron
        p1_null = r1[i] - pos_null
        p1_null_dist = np.linalg.norm(p1_null)
        p2_null = r2[i] - pos_null
        p2_null_dist = np.linalg.norm(p2_null)
        p3_null = r3[i] + pos_null
        p3_null_dist = np.linalg.norm(p3_null)
        p4_null = r4[i] - pos_null
        p4_null_dist = np.linalg.norm(p4_null)
        min_null_dist = np.min(np.array([p1_null_dist,p2_null_dist,p3_null_dist,p4_null_dist]))

        out_null_p1_dist[i] = p1_null_dist
        out_null_p2_dist[i] = p2_null_dist
        out_null_p3_dist[i] = p3_null_dist
        out_null_p4_dist[i] = p4_null_dist

        # Estimate field at each probe using the estimated linear gradient
        # These should all be quite close to the measured fields.

        dR1 = -1.0 * lingrad_output['dR1'][i]
        dR2 = -1.0 * lingrad_output['dR2'][i]
        dR3 = -1.0 * lingrad_output['dR3'][i]
        dR4 = -1.0 * lingrad_output['dR4'][i]

        F1_est = b0 + np.matmul(J,dR1)
        F2_est = b0 + np.matmul(J,dR2)
        F3_est = b0 + np.matmul(J,dR3)
        F4_est = b0 + np.matmul(J,dR4)

        F1_obs = np.array([bx1[i],by1[i],bz1[i]])
        F2_obs = np.array([bx2[i],by2[i],bz2[i]])
        F3_obs = np.array([bx3[i],by3[i],bz3[i]])
        F4_obs = np.array([bx4[i],by4[i],bz4[i]])

        F1_err = F1_est - F1_obs
        F2_err = F2_est - F2_obs
        F3_err = F3_est - F3_obs
        F4_err = F4_est - F4_obs

        F1_err_norm = np.linalg.norm(F1_err)
        F2_err_norm = np.linalg.norm(F2_err)
        F3_err_norm = np.linalg.norm(F3_err)
        F4_err_norm = np.linalg.norm(F4_err)

        max_reconstruction_error = np.max(np.array([F1_err_norm,F2_err_norm,F3_err_norm,F4_err_norm]))
        out_max_reconstruction_error[i] = max_reconstruction_error

        # Look for opposite signs in each field component, necessary if null is within tetrahedron
        bxmax = np.max( (F1_obs[0],F2_obs[0],F3_obs[0],F4_obs[0]))
        bxmin = np.min( (F1_obs[0],F2_obs[0],F3_obs[0],F4_obs[0]))
        bymax = np.max( (F1_obs[1],F2_obs[1],F3_obs[1],F4_obs[1]))
        bymin = np.min( (F1_obs[1],F2_obs[1],F3_obs[1],F4_obs[1]))
        bzmax = np.max( (F1_obs[2],F2_obs[2],F3_obs[2],F4_obs[2]))
        bzmin = np.min( (F1_obs[2],F2_obs[2],F3_obs[2],F4_obs[2]))

        tstring = time_string(times[i])

        # Get eigenvalues of J to characterize field topology near the null
        eigenvalues, eigenvectors = np.linalg.eig(J)
        lambdas = eigenvalues
        l1_norm = np.linalg.norm(lambdas[0])
        l2_norm = np.linalg.norm(lambdas[1])
        l3_norm = np.linalg.norm(lambdas[2])
        eig_sum_norm = np.linalg.norm(lambdas[0] + lambdas[1] + lambdas[2])
        eig_max_norm = np.max((l1_norm,l2_norm,l3_norm))
        # Determine the toplogical type of the null by inspecting the eigenvalues
        typecode = classify_null_type(lambdas)
        out_typecode[i] = typecode

        # div B should be close to 0 (exactly 0 in theory), so the difference from 0 is a measure of how
        # credible any null we've found might be.  We normalize it, dividing by the magnitude of the curl,
        # to get the statistic eta.  eta < 0.40 for a credible null.
        divB = lingrad_output['LD'][i]
        LCx = lingrad_output['LCxB'][i]
        LCy = lingrad_output['LCyB'][i]
        LCz = lingrad_output['LCzB'][i]
        curlB = np.array([LCx,LCy,LCz])
        curlB_norm = np.linalg.norm(curlB)
        # eta - | del dot B| /  |del x B|
        eta = np.abs(divB)/curlB_norm
        out_null_eta[i] = eta

        # Similarly, the sum of the eigenvectors of the Jacobian gives another figure of merit.  Here,
        # we normalize by dividing the norm of the sum by the norm of the largest eigenvalue to yield xi.
        # xi < 0.40 if we trust the topology derived from the eigenvalues.  Larger values may mean that the type of
        # null detected (radial vs. spiral, etc) may be an artifact.

        xi = eig_sum_norm/eig_max_norm
        out_null_xi[i] = xi

        show_in_box = False
        if show_in_box and (bxmax*bxmin < 0.0) and (bymax*bymin < 0.0) and (bzmax*bzmin < 1.0):
            print("Null of type ",typecode_strings[typecode]," may be in tetrahedron at time ",tstring )
            if times[i] > time_double('2003-08-17/16:41:55.43'):
                print("Jacobian:")
                print(LGBx)
                print(LGBy)
                print(LGBz)
                print("Eigenvalues:")
                for l in lambdas: print(l)
                print("Eigenvectors:")
                for e in eigenvectors: print(e)
                print("r_null", r_null)
                print("Max reconstruction error:",max_reconstruction_error)
                print("Distance from null to nearest spacecraft",min_null_dist)
                print("eta:", eta)
                print("xi",xi)


    # Now create output tplot variables and set some plot options

    pos_coords = get_coords(positions[0])
    pos_units = get_units(positions[0])
    field_coords = get_coords(fields[0])
    field_units = get_units(fields[0])
    store_data('null_pos',data={'x':times,'y':out_pos_null})
    set_units('null_pos',pos_units)
    set_coords('null_pos',pos_coords)

    store_data('null_bary_dist',data={'x':times,'y':out_null_bary_dist})
    set_units('null_bary_dist',pos_units)
    set_coords('null_bary_dist',pos_coords)
    options('null_bary_dist','yrange',[0.0, 1000.0])
    options('null_bary_dist','ytitle','Null dist')

    # Create a set of variables with each null type, so we can plot each type with a different symbol
    symvars = ['null_bary_dist']
    symvars_colors = ['k']
    symvars_legends = ['Distance']
    symvars_markers = ["none"]
    all_idx=np.arange(len(out_typecode))
    for i in range(11):
        cond = out_typecode == i
        idx = all_idx[cond]
        if len(idx) > 0:
            tvar = 'null_type'+str(i)
            store_data(tvar,data={'x':times[idx],'y':out_null_bary_dist[idx]})
            options(tvar, 'marker',typecode_symbols[i])
            options(tvar,'markersize',10)
            #options(tvar, 'color',typecode_colors[i])
            options(tvar,'symbols',True)
            symvars_colors.append(typecode_colors[i])
            symvars_legends.append(typecode_strings[i])
            symvars_markers.append(typecode_symbols[i])
            symvars.append(tvar)
    # Make a pseudovariable combining the different typecodes, so we get a line plot from magnull_null_bary_distance,
    # and a scatter plot of the symbols showing the null classification types, all in one panel.
    store_data('null_bary_dist_types',data=symvars)
    options('null_bary_dist_types','color',symvars_colors)
    options('null_bary_dist_types','legend_names',symvars_legends)
    options('null_bary_dist_types','legend_location','upper right')
    options('null_bary_dist_types','legend_ncols',len((symvars)))
    options('null_bary_dist_types','legend_markerfirst',True)
    options('null_bary_dist_types','legend_markersize', 1)
    options('null_bary_dist_types','ytitle','Null types')
    set_units('null_bary_dist_types',pos_units)

    # Distances from null to each probe
    p_distances = np.stack((out_null_p1_dist,out_null_p2_dist,out_null_p3_dist,out_null_p4_dist),axis=1)
    store_data('null_sc_distances',data={'x':times,'y':p_distances})
    set_units('null_sc_distances',pos_units)
    options('null_sc_distances','color',['k','r','g','b'])
    options('null_sc_distances', 'yrange', [0.0, 1000.0])
    options('null_sc_distances','ytitle','Null-sc dist')
    options('null_sc_distances','legend_names',['P1','P2','P3','P4'])
    options('null_sc_distances','legend_ncols',4)

    store_data('null_eta', data={'x':times, 'y':out_null_eta})
    options('null_eta','yrange',[0.0,2.0])
    options('null_eta','ytitle',r"$\eta$")
    store_data('null_xi', data={'x':times, 'y':out_null_xi})
    options('null_xi','yrange',[0.0,2.0])
    options('null_xi','ytitle',r'$\xi$')

    merits = np.stack((out_null_eta,out_null_xi),axis=1)
    store_data('null_fom', data={'x':times, 'y':merits})
    options('null_fom','color',['k','m'])
    options('null_fom','yrange',[0.0,2.0])
    options('null_fom','ytitle','Quality')
    options('null_fom','legend_names',[r'$\eta$',r'$\xi$'])
    options('null_fom','legend_location','upper right')
    options('null_fom','legend_markerfirst',True)

    #print('Minimum typecode:',np.min(out_typecode))
    store_data('null_typecode',{'x':times,'y':out_typecode})
    options('null_typecode','ytitle','Null types')
    options('null_typecode','yrange',[0.0,11.0])

    store_data('max_reconstruction_error',data={'x':times,'y':out_max_reconstruction_error})
    options('max_reconstruction_error','ytitle','Max error')
    set_units('max_reconstruction_error', field_units)

    return_vars = ['null_pos', 'null_bary_dist', 'null_bary_dist_types', 'null_sc_distances', 'null_fom','null_typecode', 'max_reconstruction_error']

    return return_vars