import math
import numpy as np


class SpinmodelSegment:
    """ An object describing a single segment of a spin model.

    Attributes:
        t1 (float): Start time of segment (seconds since epoch)
        t2 (float): End time of segment (seconds since epoch)
        c1 (int): Spin count at start of segment
        c2 (int): Spin count at end of segment
        b (float): Initial spin rate in degrees/sec
        c (float): Acceleration of spin rate in degrees/sec^2
        npts (int): Number of data points used to construct this segment
        maxgap (float): Largest gap, in seconds, in data used to construct this segment
        phaserr (float): The maximum fitting error in this segment (seconds)
        initial_delta_phi (float): The offset in degrees between the corrected spin model and uncorrected IDPU model at
            the start of the segment
        idpu_spinper (float): The onboard spin period during an eclipse segment
        segflags (int): Bit mapped flags describing the eclipse and correction status during this segment
            Bit 0 (lsb) eclipse flag, bit 1 waveform corrections applied, bit 2 spin fit corrections applied
    """

    __slots__ = 't1', 't2', 'c1', 'c2', 'b', 'c', 'npts', 'maxgap', 'phaserr', 'initial_delta_phi', 'idpu_spinper', \
                'segflags'

    def __init__(self,
                 t1: float,
                 t2: float,
                 c1: int,
                 c2: int,
                 b: float,
                 c: float,
                 npts: int,
                 maxgap: float,
                 phaserr: float,
                 initial_delta_phi: float,
                 idpu_spinper: float,
                 segflags: int):
        self.t1 = t1
        self.t2 = t2
        self.c1 = np.int32(c1)
        self.c2 = np.int32(c2)
        self.b = b
        self.c = c
        self.npts = npts
        self.maxgap = maxgap
        self.phaserr = phaserr
        self.initial_delta_phi = initial_delta_phi
        self.idpu_spinper = idpu_spinper
        self.segflags = segflags

    def print(self):
        """ Print a segment using sensible formatting

        Args:

        Returns:
         """

        print('%20.8f %20.8f %d %d %f %e %d %f %f %f %f %d' % (self.t1, self.t2, self.c1, self.c2,
                                                               self.b, self.c, self.npts, self.maxgap, self.phaserr,
                                                               self.initial_delta_phi,
                                                               self.idpu_spinper, self.segflags))

# Previously, this module included a set of interpolation and extrapolation routines for
# single spinmodel segments:
#
# extrap_before_t()
# extrap_after_t()
# extrap_before_n()
# extrap_after_n()
#
# These routines have been inlined where needed, and users should be calling the interp_t or interp_n methods on
# the spinmodel object.   If needed, the removed routines can be restored from the version history, or the IDL code.
# JWL 2023-03-13
#

    def interp_t(self,
                 t: float) -> (float, float, int, float, float):
        """Return modeled values for a time falling within the segment start/end times

        Args:
            t (float): Input time (seconds since epoch)

        Returns:
            A tuple containing the modeled spin period, spin count, spin phase, eclipse_delta_phi, and t_last
                at the input time.

        """

        dt = t - self.t1
        phi = (self.b * dt + self.c * dt * dt)
        bp = self.b + 2.0 * self.c * dt
        spinper = 360.0 / bp
        spincount, spinphase = divmod(phi, 360.0)
        fracspins = phi / 360.0
        phi_lastpulse = spincount * 360.0
        if abs(self.c) < 1.0e-12:
            tlast_dt = phi_lastpulse / self.b
        else:
            b = self.b
            c = self.c
            tlast_dt = (-b + math.sqrt(b * b - 4.0 * c * (-phi_lastpulse))) / (2.0 * c)
        if ((self.segflags & 3) == 3) and (self.idpu_spinper > 1.0):
            model_phi = fracspins * 360.0
            idpu_bp = 360.0 / self.idpu_spinper
            idpu_phi = dt * idpu_bp
            eclipse_delta_phi = self.initial_delta_phi + (model_phi - idpu_phi)

        else:
            eclipse_delta_phi = 0.0
        t_last = self.t1 + tlast_dt
        spincount = spincount + self.c1
        return spinper, spinphase, spincount, eclipse_delta_phi, t_last



