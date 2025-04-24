import numpy as np
from pyspedas.cotrans_tools.cart_to_sphere import cart_to_sphere
from pyspedas.cotrans_tools.sphere_to_cart import sphere_to_cart

def spd_pgs_v_shift(data, vector):
# Procedure:
# spd_pgs_v_shift
# 
# Purpose:
#   Shift a single distribution strucure by a specified velocity vector
# 
# Input:
#   data:  Sanitized particle data structure to be operated on
#   vector:  3-vector in km/s
#   matrix:  (optional) rotation matrix to apply to vector before shift
# 
# Output:
#   error:  flag, 1 indicates error, 0 none
# 
# Notes:
#   -Particle velocities are assumed to be small enough 
#    to use classical calculation.
# 

# Ensure vector has exactly 3 elements
    if len(vector) != 3:
        return

# If matrix has 9 elements, do matrix-vector multiplication
    #if matrix.size == 9:
        #vector = matrix.reshape(3, 3) @ vector

    # calculate bin velocities
    # distribution mass in eV/(km/s)^2
    v = np.sqrt(2.0 * data['energy']/data['mass'])
    theta = data['theta']
    phi = data['phi']

    #sphere to cart
    x, y, z = sphere_to_cart(v, theta, phi)

    #subtract input vector
    newx = x - vector[0]
    newy = y - vector[1]
    newz = z - vector[2]    

    #cart to sphere
    v_new, theta, phi = cart_to_sphere(newx, newy, newz)
    data['energy'] = .5 * data['mass'] * v_new**2
    data['theta'] = theta
    data['phi'] = phi
