import numpy as np
import logging
from .lingradest import lingradest
from pyspedas import tinterpol
from pytplot import get_data, store_data, time_double, time_string, time_clip, deflag, tnames, options, tplot_options, tsmooth

def find_magnetic_nulls_fote(positions=None, fields=None, scale_factor=1.0):
    """
    Find magnetic null points, given a set of four-point magnetic field observations (e.g. MMS or CLUSTER) using the
    First Order Taylor Expansion (FOTE) method.

    This method uses tetrahedral interpolation to estimate the magnetic field (B0) and field gradients at the tetrahedron
    barycenter. From the field gradients we can construct a Jacobian matrix (J).  The field in that region can be
    expressed, to a first order approximation, as

    B = B0 + JV

    where V is the position vector relative to the barycenter.  At a magnetic null V_null, all components of B are zero,
    so we have

    [0] = B0 + JV_null

    so that

    V_null = J_inv[-B0]

    As long as the four field measurements all differ, a null point will always be found.   For it to be credible,
    it should be in the neighborhood where the linear gradient approximation is expected to be valid.

    The topology of the field around the null can be inferred from the eigenvalues and eigenvectors of the
    estimated Jacobian.

    Parameters
    -----------

    positions: list of str
        A 4-element list of tplot variable names representing the probe positions

    fields: list of str
        A 4-element list of tplot variable names representing the magnetic field measurements

    scale_factor: float
        The scale factor passed lingradest routine to scale some of the distances
        Default: 1.0

    Returns
    -------
    A list of tplot variables describing the nulls found


    Example:
    >>> import pyspedas
    >>> from pytplot
    >>> # load data and ephemeris
    >>> pyspedas.find_magnetic_nulls_fote(positions,fields)
    """

    # Input data needs to be sanitized, by removing any 'nans', and finding a time range common
    # to all the deflagged variables

    positions_df = []
    fields_df = []
    fields_sm = []
    for i in range(4):
        positions_df.append(positions[i]+'_df')
        fields_df.append(fields[i]+'_df')
        # Smoothing
        fields_sm.append(fields[i]+'_sm')
        # No smoothing
        #fields_sm.append(fields[i]+'_df')

        deflag(positions[i], method='remove_nan', new_tvar=positions_df[i])
        deflag(fields[i], method='remove_nan', new_tvar=fields_df[i])
        # We'll try smoothing the fields, too
        tsmooth(fields_df[i], width=10, median=True, new_names=fields_sm[i])


    #print(tnames('*_df'))
    #print(tnames('*_sm'))
    d=get_data(fields_sm[1])
    #print(d.y[-1])
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
    time_clip(fields_sm[0], tmin, tmax, new_names='f0_tc')

    # Now we can interpolate safely
    tinterpol(positions_df,'f0_tc',newname=['pos1_i','pos2_i','pos3_i','pos4_i'])
    tinterpol(fields_sm, 'f0_tc', newname=['b1_i','b2_i','b3_i','b4_i'])
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

    # Get the data arrays from the interpolated tplot variables

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
        J = np.stack((LGBx, LGBy, LGBz))  # Jacobian matrix (or its transpose?)
        J_inv = np.linalg.inv(J)

        # Solve for null position with respect to barycenter (maybe check for singular matrix first?)

        r_null = np.linalg.solve(J,b0_neg)
        r_null_alt = np.matmul(J_inv,b0_neg)# Check that estimated field at null is near 0
        F_null = b0 + np.matmul(J,r_null)
        F_null_alt = b0 + np.matmul(J,r_null_alt)
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

        out_null_p1_dist[i] = p1_null_dist
        out_null_p2_dist[i] = p2_null_dist
        out_null_p3_dist[i] = p3_null_dist
        out_null_p4_dist[i] = p4_null_dist

        # Estimate field at each probe using the estimated linear gradient
        # Might need to be negated for correct sense of distances?
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

        # Look for opposite signs in each field component, necessary if null is within tetrahedron
        bxmax = np.max( (F1_obs[0],F2_obs[0],F3_obs[0],F4_obs[0]))
        bxmin = np.min( (F1_obs[0],F2_obs[0],F3_obs[0],F4_obs[0]))
        bymax = np.max( (F1_obs[1],F2_obs[1],F3_obs[1],F4_obs[1]))
        bymin = np.min( (F1_obs[1],F2_obs[1],F3_obs[1],F4_obs[1]))
        bzmax = np.max( (F1_obs[2],F2_obs[2],F3_obs[2],F4_obs[2]))
        bzmin = np.min( (F1_obs[2],F2_obs[2],F3_obs[2],F4_obs[2]))

        tstring = time_string(times[i])
        #if (bxmax*bxmin < 0.0) and (bymax*bymin < 0.0) and (bzmax*bzmin < 1.0):
        #    print("Null may be in tetrahedron at time ",tstring )
        #    print("F1 obs:", F1_obs)
        #    print("F2 obs:", F2_obs)
        #    print("F3 obs:", F3_obs)
        #    print("F4 obs:", F4_obs)
        #    print("r_null", r_null)




        # Get eigenvalues of J to characterize field topology near the null
        eigenvalues, eigenvectors = np.linalg.eig(J)
        lambdas = eigenvalues
        l1_norm = np.linalg.norm(lambdas[0])
        l2_norm = np.linalg.norm(lambdas[1])
        l3_norm = np.linalg.norm(lambdas[2])
        eig_sum_norm = np.linalg.norm(lambdas[0] + lambdas[1] + lambdas[2])
        eig_max_norm = np.max((l1_norm,l2_norm,l3_norm))

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

    store_data('magnull_pos',data={'x':times,'y':out_pos_null})
    store_data('magnull_pos_bary',data={'x':times,'y':out_pos_bary})
    store_data('magnull_null_bary_dist',data={'x':times,'y':out_null_bary_dist})
    options('magnull_null_bary_dist','yrange',[0.0, 5000.0])
    print('Minimum null distance:',np.min(out_null_bary_dist))
    store_data('magnull_null_p1_dist',data={'x':times,'y':out_null_p1_dist})
    store_data('magnull_null_p2_dist',data={'x':times,'y':out_null_p2_dist})
    store_data('magnull_null_p3_dist',data={'x':times,'y':out_null_p3_dist})
    store_data('magnull_null_p4_dist',data={'x':times,'y':out_null_p4_dist})
    store_data('magnull_eta', data={'x':times, 'y':out_null_eta})
    store_data('magnull_xi', data={'x':times, 'y':out_null_xi})

    return_vars = ['magnull_pos', 'magnull_null_bary_dist', 'magnull_eta', 'magnull_xi']

    return return_vars