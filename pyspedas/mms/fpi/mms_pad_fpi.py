from copy import deepcopy
import numpy as np
from scipy.ndimage.interpolation import shift
from scipy.constants import c as const_c
from pyspedas import time_double
from pyspedas.particles.spd_slice2d.slice2d_nearest import slice2d_nearest
from pyspedas.particles.spd_slice2d.slice2d_intrange import slice2d_intrange
from pyspedas.particles.spd_slice2d.slice2d_get_support import slice2d_get_support
from pyspedas.particles.spd_slice2d.slice2d_s2c import slice2d_s2c
from pyspedas.particles.spd_slice2d.tplot_average import tplot_average
from pyspedas.mms.particles.moka_mms_clean_data import moka_mms_clean_data


def mms_pad_fpi(dists,
                #disterr,
                time=None,
                window=None,
                center_time=False,
                trange=None,
                samples=None,
                mag_data=None,
                vel_data=None,
                nbin=18,
                da=45.0,
                da2=45.0,
                pr___0=None,
                pr__90=None,
                pr_180=None,
                subtract_bulk=False,
                units='df_cm',
                oclreal=False,
                norm=False):
    """

    """

    dr = np.pi/180.0
    rd = 1.0/dr

    if pr___0 is None:
        pr___0 = [0.0, da]  # para pitch angle range
    if pr__90 is None:
        pr__90 = [90-da2, 90+da2]  # perp pitch angle range
    if pr_180 is None:
        pr_180 = [180-da, 180.0]  # anti-para pitch angle range

    if trange is None:
        if time is None:
            print('Please specifiy a time or time range over which to compute the pad.  For example: ')
            print('  "time=t, window=w" or "trange=tr" or "time=t, samples=n"')
            return
        if window is None and samples is None:
            samples = 1  # use single closest distribution by default
    else:
        # time range already provided
        trange = [np.nanmin(time_double(trange)), np.nanmax(time_double(trange))]

    if time is not None:
        # get the time range if one was specified
        time = time_double(time)

    # get the time range if a time & window were specified instead
    if trange is None and window is not None:
        if center_time:
            trange = [time - window/2.0, time + window/2.0]
        else:
            trange = [time, time + window]

    # if no time range or window was specified then get a time range
    # from the N closest samples to the specified time
    #   (defaults to 1 if SAMPLES is not defined)
    if trange is None:
        trange = slice2d_nearest(dists, time, samples)

    # check that there is data in the trange before proceeding
    times_ind = slice2d_intrange(dists, trange)

    n_samples = len(times_ind)

    if n_samples < 1:
        print('No particle data in the time window; ')
        print('Time samples may be at low cadence; try adjusting the time window.')
        return

    print(str(n_samples) + ' samples in time window')

    nns = np.nanmin(times_ind)
    nne = np.nanmax(times_ind)

    # check support data
    bfield = slice2d_get_support(mag_data, trange)
    vbulk = slice2d_get_support(vel_data, trange)

    if bfield is None:
        print('Magnetic field data needed to calculate pitch-angles')
        return
    if vbulk is None and subtract_bulk:
        print('Velocity data needed to subtract bulk velocity.')
        return

    species = dists[0]['species']
    if units == 'eflux':
        if species == 'i':
            A = 1  # H+
        elif species == 'e':
            A = 1.0/1836.0

        flux_to_df = A**2 * 0.5447*1e6
        cm_to_km = 1e30
        in_u = np.array([2, -1, 0]) # units_in = 'df_km'
        out_u = np.array([0, 0, 0]) # units_out = 'eflux'
        exp = in_u + out_u


    # pitch angle bins
    kmax = nbin
    pamin = 0.0
    pamax = 180.0
    dpa = (pamax-pamin)/kmax  # bin size
    wpa = pamin + np.arange(kmax)*dpa + 0.5*dpa  # bin center values
    pa_bin = np.append(pamin + np.arange(kmax)*dpa, pamax)

    # azimuthal bins
    amax = 16
    azmin = 0.
    azmax = 180.
    daz = (azmax-azmin)/amax
    waz = azmin + np.arange(amax) * daz + 0.5 * daz
    az_bin = np.append(azmin + np.arange(amax) * daz, azmax)

    # polar bins
    pmax = 16
    polmin = 0.
    polmax = 360.
    dpol = (polmax - polmin)/pmax
    wpol = polmin + np.arange(pmax) * dpol + 0.5 * dpol
    pol_bin = np.append(polmin + np.arange(pmax) * dpol, polmax)

    # PA (az x pol)
    pa_azpol = np.zeros((amax, pmax))
    pa_azpol[:, :] = np.nan

    # energy bins
    wegy = dists[0]['energy'][:, 0, 0]
    if subtract_bulk:
        wegy = np.append(2 * wegy[0] - wegy[1], wegy)

    jmax = len(wegy)
    egy_bin = 0.5*(wegy + shift(wegy, -1))
    egy_bin[jmax - 1] = 2. * wegy[jmax - 1] - egy_bin[jmax - 2]
    egy_bin0 = 2. * wegy[0] - egy_bin[0]
    if egy_bin0 < 0:
        egy_bin0 = 0
    egy_bin = np.append(egy_bin0, egy_bin)

    # prep
    pad = np.zeros((jmax, kmax))
    mmax = 4
    f_dat = np.zeros((jmax, mmax)) # Four elements for para, perp, anti-para and omni directions
    f_psd = np.zeros((jmax, mmax))
    f_err = np.zeros((jmax, mmax))
    f_cnt = np.zeros((jmax, mmax))
    count_pad = np.zeros((jmax, kmax))
    count_dat = np.zeros((jmax, mmax))

    # magnetic field and bulk velocity
    bnrm_avg = [0., 0., 0.]
    babs_avg = 0.
    vbulk_avg = [0.0, 0.0, 0.0]
    vbulk_para = 0.0
    vbulk_perp = 0.0
    vbulk_vxb = 0.0
    vbulk_exb = 0.0

    # main loop
    iecl = 0
    iecm = 0

    for n in np.arange(nns, nne+1):
        data = moka_mms_clean_data(dists[n], units=units)

        # magnetic field direction
        tr = [dists[n]['start_time'], dists[n]['end_time']]
        bfield = tplot_average(mag_data, tr, quiet=True)
        babs = np.sqrt(bfield[0]**2 + bfield[1]**2 + bfield[2]**2)
        bnrm = bfield/babs
        bnrm_avg += bnrm
        babs_avg += babs

        # bulk velocity
        if not subtract_bulk:
            vbulk = np.array([0.0, 0.0, 0.0])

        vbpara = bnrm[0]*vbulk[0]+bnrm[1]*vbulk[1]+bnrm[2]*vbulk[2]
        vbperp = vbulk - vbpara
        vbperp_abs = np.sqrt(vbperp[0]**2+vbperp[1]**2+vbperp[2]**2)
        vxb = np.array([-vbulk[1]*bnrm[2]+vbulk[2]*bnrm[1], -vbulk[2]*bnrm[0]+vbulk[0]*bnrm[2], -vbulk[0]*bnrm[1]+vbulk[1]*bnrm[0]])
        vxbabs = np.sqrt(vxb[0]**2+vxb[1]**2+vxb[2]**2)
        vxbnrm = vxb/vxbabs
        exb = np.array([vxb[1]*bnrm[2]-vxb[2]*bnrm[1],vxb[2]*bnrm[0]-vxb[0]*bnrm[2],vxb[0]*bnrm[1]-vxb[1]*bnrm[0]])
        exbabs = np.sqrt(exb[0]**2+exb[1]**2+exb[2]**2)
        exbnrm = exb/exbabs
        vbulk_para += vbpara
        vbulk_perp += vbperp_abs
        vbulk_vxb += vxbnrm[0]*vbulk[0]+vxbnrm[1]*vbulk[1]+vxbnrm[2]*vbulk[2]
        vbulk_exb += exbnrm[0]*vbulk[0]+exbnrm[1]*vbulk[1]+exbnrm[2]*vbulk[2]
        vbulk_avg += vbulk

        # particle velocities & pitch angles

        # spherical to cartesian
        erest = data['mass']*const_c**2/1e6  # convert mass from eV/(km/s)^2 to eV
        vabs = const_c*np.sqrt(1 - 1/((data['energy']/erest + 1)**2))/1000.0
        vdata = slice2d_s2c(vabs, data['theta'], data['phi'])
        vx = vdata[:, 0]
        vy = vdata[:, 1]
        vz = vdata[:, 2]

        if subtract_bulk:
            vx -= vbulk[0]
            vy -= vbulk[1]
            vz -= vbulk[2]

        # pitch angles
        dp = (bnrm[0]*vx + bnrm[1]*vy + bnrm[2]*vz)/np.sqrt(vx**2+vy**2+vz**2)
        dp[dp > 1.0] = 1.0
        dp[dp < -1.0] = -1.0
        pa = rd*np.arccos(dp)

        # Cartesian to spherical
        vnew, theta, phi = cart_to_sphere(vx, vy, vz)
        data['energy'] = erest*(1.0/np.sqrt(1.0-(vnew*1000.0/const_c)**2)-1.0)  # eV
        data['phi'] = phi
        data['theta'] = theta
        data['pa'] = pa

        azang = 90.0 - data['theta']

        imax = len(data['data_dat'])

        for i in np.arange(0, imax):
            # find energy bin
            j = np.nanargmin(np.abs(egy_bin-data['energy'][i]))
            if egy_bin[j] > data['energy'][i]:
                j -= 1
            if j == jmax:
                j -= 1

            # find pitch-angle bin
            k = np.nanargmin(np.abs(pa_bin-data['pa'][i]))
            if pa_bin[k] > data['pa'][i]:
                k -= 1
            if k == kmax:
                k -= 1

            # find azimuthal bin
            a = np.nanargmin(np.abs(az_bin-azang[i]))
            if az_bin[a] > azang[i]:
                a -= 1
            if a == amax:
                a -= 1

            # find polar bin
            p = np.nanargmin(np.abs(pol_bin-data['phi'][i]))
            if pol_bin[p] > data['phi'][i]:
                p -= 1
            if p == pmax:
                p -= 1

            if j >= 0:
                pa_azpol[a, p] = data['pa'][i]

                # find new eflux
                # If shifted to plasma rest-frame, 'eflux' should be re-evaluated
                # from 'psd' because 'eflux' depends on the particle energy. We don't need to
                # worry about this if we want the output in 'psd'.
                newenergy = wegy[j]
                if units == 'eflux':
                    newdat = data['data_psd'][i]*newenergy**exp[0]*(flux_to_df**exp[1]*cm_to_km**exp[2])
                    newpsd = newdat
                    newerr = data['data_err'][i]*newenergy**exp[0]*(flux_to_df**exp[1]*cm_to_km**exp[2])
                else:
                    newdat = data['data_dat'][i]
                    newpsd = data['data_psd'][i]
                    newerr = data['data_err'][i]

                pad[j, k] += newdat
                count_pad[j, k] += 1

                # energy spectrum (para, perp, anti-para)
                m = -1
                if (pr__90[0] <= data['pa'][i]) and (data['pa'][i] <= pr__90[1]):
                    m = 1
                else:
                    if (pr___0[0] <= data['pa'][i]) and (data['pa'][i] <= pr___0[1]):
                        m = 0
                    if (pr_180[0] <= data['pa'][i]) and (data['pa'][i] <= pr_180[1]):
                        m = 2

                if (m >= 0) and (m <= 2):
                    f_dat[j, m] += newdat
                    f_psd[j, m] += newpsd
                    f_err[j, m] += newerr
                    f_cnt[j, m] += data['data_cnt'][i]
                    count_dat[j, m] += 1

                # energy spectrum (omni-direction)
                m = 3
                f_dat[j, m] += newdat
                f_psd[j, m] += newpsd
                f_err[j, m] += newerr
                f_cnt[j, m] += data['data_cnt'][i]
                count_dat[j, m] += 1
            else:
                iecl += 1
        else:
            iecm += imax

    pad /= count_pad
    f_dat /= count_dat
    f_psd /= count_dat
    f_err /= count_dat
    f_cnt /= count_dat

    vbulk_para /= float(n_samples)
    vbulk_perp /= float(n_samples)
    vbulk_vxb /= float(n_samples)
    vbulk_exb /= float(n_samples)
    vbulk_avg /= float(n_samples)

    bnrm_avg /= float(n_samples)
    babs_avg /= float(n_samples)

    pad = np.nan_to_num(pad, nan=0)

    # angle padding
    padnew = np.zeros((jmax, kmax+2))
    padnew[0:jmax, 1:kmax+1] = pad
    padnew[0:jmax, 0] = padnew[0:jmax, 1]
    padnew[0:jmax, kmax + 1] = padnew[0:jmax, kmax]
    pad = padnew
    wpa_new = np.append(wpa[0] - dpa, wpa)
    wpa_new = np.append(wpa_new, wpa[kmax - 1] + dpa)
    wpa = wpa_new

    # normalize
    padnorm = deepcopy(pad)
    for j in range(0, jmax):
        peak = np.nanmax(pad[j, 0:kmax])  # find the peak
        if peak == 0:
            padnorm[j, 0:kmax] = 0.0
        else:
            padnorm[j, 0:kmax] /= peak

    if norm:
        pad = padnorm

    # Effective one-count-level
    # 'f_psd' is the PSD    averaged over time and angular ranges.
    # 'f_cnt' is the counts averaged over time and angular ranges.
    # 'count_dat is the total number of time and angular bins.
    if oclreal:
        f_ocl = f_psd/f_cnt
    else:
        f_ocl = f_psd/(f_cnt*count_dat)

    # output
    return {'trange': trange,
            'egy': wegy,
            'pa': wpa,
            'data': pad,
            'datanorm': padnorm,
            'numSlices': n_samples,
            'nbin': kmax,
            'units': units,
            'subtract_bulk': subtract_bulk,
            'egyrange': [np.nanmin(wegy), np.nanmax(wegy)],
            #'parange': [np.nanmin(wpa), np.nanmax(wpa)],
            'spec___0': f_psd[:, 0],
            'spec__90': f_psd[:, 1],
            'spec_180': f_psd[:, 2],
            'spec_omn': f_psd[:, 3],
            'cnts___0': f_cnt[:, 0],
            'cnts__90': f_cnt[:, 1],
            'cnts_180': f_cnt[:, 2],
            'cnts_omn': f_cnt[:, 3],
            'oclv___0': f_ocl[:, 0],
            'oclv__90': f_ocl[:, 1],
            'oclv_180': f_ocl[:, 2],
            'oclv_omn': f_ocl[:, 3],
            'eror___0': f_err[:, 0],
            'eror__90': f_err[:, 1],
            'eror_180': f_err[:, 2],
            'eror_omn': f_err[:, 3],
            'vbulk_para': vbulk_para,
            'vbulk_perp_abs': vbulk_perp,
            'vbulk_vxb': vbulk_vxb,
            'vbulk_exb': vbulk_exb,
            'bnrm': bnrm_avg,
            'Vbulk': vbulk_avg,
            'bfield': bnrm_avg * babs_avg,
            'species': species,
            'pa_azpol': pa_azpol,
            'wpol': wpol,
            'waz': waz}


def cart_to_sphere(x, y, z):
    rho = x * x + y * y
    r = np.sqrt(rho + z * z)
    phi = 18e1/np.pi * np.arctan2(y, x)
    # should be between 0-360
    phi[phi < 0] += 360.0
    theta = 18e1/np.pi * np.arctan(z / np.sqrt(rho))
    return (r, theta, phi)