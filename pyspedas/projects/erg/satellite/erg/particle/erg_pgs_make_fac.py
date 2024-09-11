import numpy as np

from pyspedas import tcopy
from pytplot import get_data, store_data, tnames

from pyspedas.cotrans_tools.cotrans import cotrans
from pytplot import tnormalize
from pytplot import tcrossp
from pyspedas.analysis.tinterpol import tinterpol

from ..common.cotrans.erg_cotrans import erg_cotrans

# ;so we don't have one long routine of doom, all transforms should be separate helper functions
def erg_pgs_xgse(
    mag_temp,
    pos_tmp=None
):
    
    mag_data = get_data(mag_temp)

    # xaxis of this system is X of the gse system. Z is mag field
    x_axis = np.zeros((len(mag_data.times), 3))
    x_axis[:, 0] = 1
    
    store_data('xgse_pgs_temp', data={'x':mag_data[0], 'y':x_axis})
    cotrans('xgse_pgs_temp', name_out='xgse_pgs_temp',
            coord_in='gse', coord_out='j2000')
    erg_cotrans(in_name='xgse_pgs_temp', out_name='xgse_pgs_temp',
                in_coord='j2000', out_coord='dsi')
    
    # ;create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    y_basis = tcrossp(z_basis, 'xgse_pgs_temp', return_data=True)
    y_basis = tnormalize(y_basis, return_data=True)
    x_basis = tcrossp(y_basis, z_basis, return_data=True)
    
    return (x_basis, y_basis, z_basis)

# ;so we don't have one long routine of doom, all transforms should be separate helper functions
def erg_pgs_phigeo(
    mag_temp,
    pos_temp
):
    
    postmp = 'pos_pgs_temp'
    tcopy(pos_temp, postmp)
    cotrans(postmp, postmp, coord_in='gse', coord_out='geo')
    pos_data = get_data(postmp)
    
    # transformation to generate other_dim dim for phigeo from thm_fac_matrix_make
    # All the conversions to polar and trig simplifies to this.
    # But the reason the conversion is why this is the conversion that is done, is lost on me.
    # The conversion swaps the x & y components of position, reflects over x=0,z=0 then projects into the xy plane
    pos_conv = np.stack((-pos_data.y[:, 1], pos_data.y[:, 0], np.zeros(len(pos_data.times))))
    pos_conv = np.transpose(pos_conv, [1, 0])
    store_data(postmp, data={'x': pos_data.times, 'y': pos_conv})

    # ;transform into dsl because particles are in dmpa
    cotrans(postmp,postmp,coord_in='geo', coord_out='j2000')
    erg_cotrans(postmp,postmp,in_coord='j2000', out_coord='dsi')
    
    # ;create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    x_basis = tcrossp(postmp,z_basis, return_data=True)
    x_basis = tnormalize(x_basis, return_data=True)
    y_basis = tcrossp(z_basis, x_basis, return_data=True)

    return (x_basis, y_basis, z_basis)

# ;so we don't have one long routine of doom, all transforms should be separate helper functions
def erg_pgs_mphigeo(
    mag_temp,
    pos_temp
):
    
    postmp = 'pos_pgs_temp'
    tcopy(pos_temp, postmp)
    cotrans(postmp, postmp, coord_in='gse', coord_out='geo')
    pos_data = get_data(postmp)

    # the following is heisted from the IDL version
    # transformation to generate other_dim dim for mphigeo from thm_fac_matrix_make
    # All the conversions to polar and trig simplifies to this.  
    # But the reason the conversion is why this is the conversion that is done, is lost on me.
    # The conversion swaps the x & y components of position, reflects over x=0,z=0 then projects into the xy plane
    pos_conv = np.stack((pos_data.y[:, 1], -pos_data.y[:, 0], np.zeros(len(pos_data.times))))
    pos_conv = np.transpose(pos_conv, [1, 0])
    store_data(pos_temp, data={'x': pos_data.times, 'y': pos_conv})
    
    # ;transform into dsl because particles are in dmpa
    cotrans(postmp,postmp,coord_in='geo', coord_out='j2000')
    erg_cotrans(postmp,postmp,in_coord='j2000', out_coord='dsi')
    
    # ;create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    x_basis = tcrossp(z_basis, postmp, return_data=True)
    x_basis = tnormalize(x_basis, return_data=True)
    y_basis = tcrossp(z_basis, x_basis, return_data=True)
    
    return (x_basis, y_basis, z_basis)


"""
;; ERG_PGS_PHISM
;; To get unit vectors for FAC-phi_sm coordinate system
;; Z axis: local B-vector dir, usually taken from spin-averaged MGF data
;; X axis: phi_sm vector x Z, where the phi_sm lies in the azimuthally
;;         eastward direction at a spacecraft position in the SM coordinate
;;         system. In a dipole B-field geometry, X axis roughly points
;;         radially outward. 
;; Y axis: Z axis x X axis, roughly pointing azimuthally eastward
;;
;; Common to the other procedures here, pos_temp is the name of a
;; tplot variable containing spacecraft's position coordinates
;; in GSE. "mag_temp" is for the local magnetic field vectors in DSI. 
"""

def erg_pgs_phism(
    mag_temp,
    pos_temp
):
    postmp = 'pos_pgs_temp'
    tcopy(pos_temp, postmp)
    cotrans(postmp, postmp, coord_in='gse', coord_out='sm')
    pos_data = get_data(postmp)
    
    """
    ;; The conversion swaps the x & y components of position, reflects
    ;; over x=0,z=0 then projects into the xy plane. In other words, the
    ;; position vectors projected on the SM-X-Y plane are rotated by +90
    ;; degrees around the SM-Z axis to get the phi_sm vectors.
    """
    
    phitmp = 'phism_tmp'
    pos_conv = np.stack((-pos_data.y[:, 1], pos_data.y[:, 0], np.zeros(len(pos_data.times))))
    pos_conv = np.transpose(pos_conv, [1, 0])
    store_data(phitmp, data={'x': pos_data.times, 'y': pos_conv})
    #   SM to DSI 
    cotrans(phitmp, phitmp, coord_in='sm', coord_out='j2000')
    erg_cotrans(phitmp, phitmp, in_coord='j2000', out_coord='dsi')
    
    # ;; create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    x_basis = tcrossp(phitmp, z_basis, return_data=True)
    x_basis = tnormalize(x_basis, return_data=True)
    y_basis = tcrossp(z_basis, x_basis, return_data=True)
    
    #  ;; clean up the temporary variables
    store_data( [ postmp, phitmp ], delete=True)

    return (x_basis, y_basis, z_basis)

"""
;; ERG_PGS_MPHISM
;; To get unit vectors for FAC-(minus phi_sm) coordinate system
;; Z axis: local B-vector dir, usually taken from spin-averaged MGF data
;; X axis: minus phi_sm vector x Z, where the minus phi_sm lies in the azimuthally
;;         westward direction at a spacecraft position in the SM coordinate
;;         system. In a dipole B-field geometry, X axis roughly points
;;         radially inward. 
;; Y axis: Z axis x X axis, roughly pointing azimuthally westward
;;
;; Common to the other procedures here, pos_temp is the name of a
;; tplot variable containing spacecraft's position coordinates
;; in GSE. "mag_temp" is for the local magnetic field vectors in DSI. 
"""
def erg_pgs_mphism(
    mag_temp,
    pos_temp
):
    
    postmp = 'pos_pgs_temp'
    tcopy(pos_temp, postmp)
    cotrans(postmp, postmp, coord_in='gse', coord_out='sm')
    pos_data = get_data(postmp)
    
    """
    ;; The conversion swaps the x & y components of position, reflects
    ;; over x=0,z=0 then projects into the xy plane. In other words, the
    ;; position vectors projected on the SM-X-Y plane are rotated by +90
    ;; degrees around the SM-Z axis to get the phi_sm vectors.
    """
    phitmp = 'phism_tmp'  # ;; Note that the same name is used as in erg_pgs_phism(), but it has opposite vectors 
    pos_conv = np.stack((pos_data.y[:, 1], -pos_data.y[:, 0], np.zeros(len(pos_data.times))))
    pos_conv = np.transpose(pos_conv, [1, 0])
    store_data(phitmp, data={'x': pos_data.times, 'y': pos_conv})
    #  ;; SM to DSI
    cotrans(phitmp, phitmp, coord_in='sm', coord_out='j2000')
    erg_cotrans(phitmp, phitmp, in_coord='j2000', out_coord='dsi')
    
    # ;; create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    x_basis = tcrossp(phitmp, z_basis, return_data=True)
    x_basis = tnormalize(x_basis, return_data=True)
    y_basis = tcrossp(z_basis, x_basis, return_data=True)

    #  ;; clean up the temporary variables
    store_data( [ postmp, phitmp ], delete=True)

    return (x_basis, y_basis, z_basis)

def erg_pgs_xdsi(
    mag_temp,
    pos_tmp=None
):
    
    mag_data = get_data(mag_temp)

    # xaxis of this system is X of the gse system. Z is mag field
    x_axis = np.zeros((len(mag_data.times), 3))
    x_axis[:, 0] = 1.
    
    # ;create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    y_basis = tcrossp(z_basis, x_axis, return_data=True)
    y_basis = tnormalize(y_basis, return_data=True)
    x_basis = tcrossp(y_basis, z_basis, return_data=True)
    
    return (x_basis, y_basis, z_basis)

def erg_pgs_make_fac(
    times_array,
    mag_tvar_in=None,
    pos_tvar_in=None,
    fac_type='mphism'
):
    """
    Args:
        times_array (Numpy Array): ;the time grid of the particle data.
        mag_tvar_in (str): ;tplot variable containing the mag data in DSI. Defaults to None.
        pos_tvar_in (str, optional): ;position variable containing the position data in GSE. Defaults to None.
        fac_type (str, optional): ;field aligned coordinate transform type (only mphigeo, atm). Defaults to 'mphism'.
    """
    
    valid_types = ['mphigeo', 'phigeo', 'xgse', 'phism', 'mphism', 'xdsi']
    
    if fac_type not in valid_types:
        print(f'Invalid FAC type "{fac_type}"; valid types: {valid_types}')
        return
    
    if (mag_tvar_in is None) or (pos_tvar_in is None):
        print('Magnetic field and/or spacecraft position data not specified.')
        print('Please use mag_tvar_in and pos_tvar_in arguments.')
        return
    
    """
    ;;--------------------------------------------------------------------       
    ;;sanitize
    ;;--------------------------------------------------------------------
    
    ;;Note this logic could probably be rolled into
    ;;thm_pgs_clean_support in the future
    ;; Normnally mag_tvar_in should be erg_mgf_l2_mag_8sec_dsi
    """
    
    if len(tnames(mag_tvar_in)) > 0:
        mag_tvar = tnames(mag_tvar_in)[0]
        mag_temp = mag_tvar + '_pgs_temp'
        #  ;;Right now, magnetic field must be in DSI coordinates
        tcopy(mag_tvar, mag_temp)  # ;;Sanitize it
        tinterpol(mag_temp, times_array, newname=mag_temp)
    else:
        print(f'Magnetic field variable not found: "{mag_tvar_in}"')
        print('skipping field-aligned outputs')
        return
    
    #  ;; Normally pos_tvar_in should be erg_orb_l2_pos_gse
    if len(tnames(pos_tvar_in)) > 0:
        pos_tvar = tnames(pos_tvar_in)[0]
        pos_temp = pos_tvar + '_pgs_temp'
        tcopy(pos_tvar, pos_temp)  # ;;Sanitize it
        tinterpol(pos_temp, times_array, newname=pos_temp)
    else:
        print(f'Position variable not found: "{pos_tvar_in}"')
        print('skipping field-aligned outputs')
        return
    
    if fac_type == 'mphigeo':
        
        """
        ;;--------------------------------------------------------------------
        ;;mphigeo
        ;;--------------------------------------------------------------------
        """
    
        basis = erg_pgs_mphigeo(mag_temp, pos_temp)
        
    elif fac_type == 'phigeo':
        
        """
        ;;--------------------------------------------------------------------
        ;;phigeo
        ;;--------------------------------------------------------------------
        """
        
        basis = erg_pgs_phigeo(mag_temp, pos_temp)
        
    elif fac_type == 'xgse':
        
        """
        ;;--------------------------------------------------------------------
        ;;xgse
        ;;--------------------------------------------------------------------
        """
        
        #  ;;position isn't necessary for this one, but uniformity of interface and requirements trumps here
        basis = erg_pgs_xgse(mag_temp, pos_temp)
        
    elif fac_type == 'phism':
        
        """
        ;;--------------------------------------------------------------------
        ;;phism
        ;;--------------------------------------------------------------------
        """
        
        basis = erg_pgs_phism(mag_temp, pos_temp)
        
    elif fac_type == 'mphism':
        
        """
        ;;--------------------------------------------------------------------
        ;;mphism
        ;;--------------------------------------------------------------------
        """
        
        basis = erg_pgs_mphism(mag_temp,pos_temp)
        
    elif fac_type == 'xdsi':
        
        """
        ;;--------------------------------------------------------------------
        ;;xdsi
        ;;--------------------------------------------------------------------
        """
        
        basis = erg_pgs_xdsi(mag_temp,pos_temp)
        
    """
    ;;--------------------------------------------------------------------
    ;;create rotation matrix
    ;;--------------------------------------------------------------------
    """
    
    fac_output = np.zeros((len(times_array), 3, 3))
    fac_output[:, 0, :] = basis[0]
    fac_output[:, 1, :] = basis[1]
    fac_output[:, 2, :] = basis[2]

    return fac_output