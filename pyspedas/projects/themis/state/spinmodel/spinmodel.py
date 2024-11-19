import numpy as np
import math
import logging
from typing import Dict
from .spinmodel_segment import SpinmodelSegment
from pytplot import get_data, store_data
from pytplot import data_exists
from pytplot import time_string


def get_sm_data(probe: str,
                valname: str,
                correction_level: int,
                suffix: str = '') -> (np.ndarray, np.ndarray):
    """ Return the times and values for a spin model tplot variable

    Args:
        probe: Probe name, one of 'a','b','c','d','e'
        valname: The data quantity to be returned
        correction_level: 0 for no corrections, 1 for waveform corrections, 2 for spin fit corrections

    Returns:
        A tuple containing the timestamps and data values as np.ndarray objects
    """
    if correction_level == 0:
        infix = '_'
    else:
        infix = '_ecl_'
    tvar_name = 'th' + probe + '_spin' + infix + valname + suffix
    if data_exists(tvar_name):
        res = get_data(tvar_name)
        return res.times, res.y
    else:
        return None


class SpinmodelInterpTResult:
    """ An object to return the results of interpolating a spin model.

    Attributes:
        spinphase (ndarray(dtype=float)): The spin phase (in degrees) at each input time
        spincount (ndarray(dtype=int)): The count of complete spins from the start of the model, at each input time
        spinper (ndarray(dtype=float)): The spin period (in seconds) at each input time
        t_last (ndarray(dtype=float)): Time (seconds since epoch) of last sun sensor crossing before the input times
        eclipse_delta_phi (ndarray(dtype=float)): The offset in degrees between the modeled spin phase and the onboard
            spin phase during an eclipse
        segflags (ndarray(dtype=int)): A set of bit flags denoting the eclipse and correction status at each input time
        idx (ndarray(dtype=int)): The index of the spin model segment containing each input time
        dt (ndarray(dtype=float)): The delta-t in seconds between the input times and start or end time of the
            containing segment

    """

    __slots__ = 'spinphase', 'spincount', 'spinper', 't_last', 'eclipse_delta_phi', 'segflags', 'idx', 'dt'

    def __init__(self, spinphase: np.ndarray,
                 spincount: np.ndarray,
                 spinper: np.ndarray,
                 t_last: np.ndarray,
                 eclipse_delta_phi: np.ndarray,
                 segflags: np.ndarray,
                 idx: np.ndarray,
                 dt: np.ndarray):
        self.spinphase = spinphase
        self.spincount = spincount
        self.spinper = spinper
        self.t_last = t_last
        self.eclipse_delta_phi = eclipse_delta_phi
        self.segflags = segflags
        self.idx = idx
        self.dt = dt


class Spinmodel:
    """ An object describing a spin model for a given probe, time interval, and correction level
    A spinmodel is created from a set of tplot variables loaded from the THEMIS STATE CDFs. The time interval is
    covered by a list of SpinmodelSegment objects, representing a piecewise quadratic fit of phi (spin plane angle)
    versus time.  The segment data from the CDF is loaded into the seg_list during initial creation of the model, with
    some on-the-fly adjustments to account for the brief gaps that occur at UTC date boundaries.  The final segment
    list is converted to a series of ndarrays, stored in the seg_* attributes, to support efficient interpolation to
    input times.

    Attributes:
        seg_list (List of SpinmodelSegment): A list of spin model segment objects comprising the model
        lastseg (SpinmodelSegment): The most recently processed SpinmodelSegment
        seg_times (ndarray): Array of t1 values from seg_list
        seg_t2 (ndarray): Array of t2 values from seg_list
        seg_c1 (ndarray): Array of c1 values from seg_list
        seg_c2 (ndarray): Array of c2 values from seg_list
        seg_b (ndarray): Array of b values from seg_list
        seg_c (ndarray): Array of c valuse from seg_list
        seg_npts (ndarray): Array of npts values from seg_list
        seg_maxgap (ndarray): Array of maxgap values from seg_list
        seg_phaserr (ndarray): Array of phaserr values from seg_list
        seg_initial_delta_phi (ndarray): Array of initial_delta_phi values from seg_list
        seg_idpu_spinper (ndarray): Array of idpu_spinper values from seg_list
        seg_segflags (ndarray): Array of segflags values from seg_list
        seg_count (int): Count of segments

    """

    def print_segs(self):
        """ Print the list of SpinmodelSegment objects, useful for troubleshooting.

          """

        for seg in self.seg_list:
            seg.print()

    def adjust_delta_phi(self,
                         ecl_start: float,
                         ecl_end: float,
                         ecl_corr: float):
        """ Apply the level 2 (spin fit) corrections to the segments falling in an eclipse time interval.

        Args:
            ecl_start (float): Start time (seconds since epoch) of an eclipse to be processed
            ecl_end (float): End time (seconds since epoch) of an eclipse to be processed
            ecl_corr (float): Eclipse delta-phi offset (degrees) between waveform and spin fit data for this eclipse
          """

        # A segment needs to be updated if its midpoint lies in the time range ecl_start to ecl_end.
        # This is more robust against floating point roundoff errors than the previous method, which
        # compared the segment endpoints rather than the midpoints.

        seg_midpoints = (self.seg_times + self.seg_t2) / 2.0
        cond1 = ecl_start <= seg_midpoints
        cond2 = seg_midpoints <= ecl_end
        cond = cond1 & cond2
        idx = np.arange(len(self.seg_list))[cond]
        self.seg_initial_delta_phi[idx] += ecl_corr
        self.seg_segflags[idx] |= 4
        # print("Eclipse start: ", ecl_start, "Eclipse end: ", ecl_end)
        # print("First eclipse segment")
        # self.seg_list[idx[0]].print()
        # print("Last eclipse segment")
        # idx_len = len(idx)
        # self.seg_list[idx[idx_len - 1]].print()
        for si in idx:
            seg = self.seg_list[si]
            seg.initial_delta_phi += ecl_corr
            seg.segflags |= 4

    def findseg_t(self,
                  t: np.ndarray) -> np.ndarray:
        """ Return an ndarray of index values for the segments covering a set of input times

        This is a helper routine for the interp_t method.

        Args:
            t (ndarray(dtype=float): Input times

        Returns:
            ndarray(dtype=int) of indices into the seg_* attributes for each input time
         """

        idx1 = np.searchsorted(self.seg_times, t)
        idx2 = np.searchsorted(self.seg_t2, t)
        diff = (idx2 - (idx1 + 1)).nonzero()
        if len(diff) == len(t):
            logging.warning('Indices don''t match up:')
            logging.warning(idx1)
            logging.warning(idx2)
        else:
            # If any points are beyond the last segment t2, assign them to the last segment and extrapolate.
            idx_max = self.seg_count - 1
            idx_extrap = idx2 > idx_max
            idx_adjusted = idx2
            idx_adjusted[idx_extrap] = idx_max
            return idx_adjusted

    def interp_t(self,
                 t: np.ndarray,
                 use_spinphase_correction: bool = True) -> SpinmodelInterpTResult:
        """ Interpolate the spin model to a set of input times, and return an object holding the results.

        This is the workhorse routine for accessing the spin model. Clients will specify a set of input times (e.g.
        from a tplot variable to be operated on), then obtain the spin status at those times, which can be used to
        transform back and forth between SSL coordinates (spinning with the spacecraft) and DSL (despun, referenced to
        sun direction and angular momentum vector/spin axis).

        Rather than inefficiently iterating over the spinmodel segments and input times, the code performs vectorized
        operations on Numpy arrays. This is done by calculating a set of segment indices corresponding to the input time
        stamps, then replicating the segment data to match the number of input times. (So, we are trading extra memory
        usage to allow vectorized bulk calculations)  To minimize branching, several boolean conditions are evaluated,
        yielding sets of array indices matching each set of conditions. The appropriate calculations are performed in
        bulk for each set of condition indices. Finally, the various outputs are collected into a SpinmodelInterpTResult
        object and returned.

        Args:
            t (ndarray(dtype=float): Input times
            use_spinphase_correction (Boolean): Flag (defaults to True) specifying whether V03 state CDF corrections
                should be applied to the interpolation output.

        Returns:
            SpinmodelInterpTResult object containing the interpolated outputs (spinphase, spincount, spin period,
            eclipse corrections, etc)
         """

        segs_idx = self.findseg_t(t)
        n = len(segs_idx)

        my_seg_times = self.seg_times[segs_idx]
        my_seg_t2 = self.seg_t2[segs_idx]
        my_seg_b = self.seg_b[segs_idx]
        my_seg_c = self.seg_c[segs_idx]
        my_seg_c1 = self.seg_c1[segs_idx]
        my_seg_c2 = self.seg_c2[segs_idx]
        my_seg_initial_delta_phi = self.seg_initial_delta_phi[segs_idx]
        my_seg_idpu_spinper = self.seg_idpu_spinper[segs_idx]
        my_seg_segflags = self.seg_segflags[segs_idx]

        # Below this point, all indexing assumes n = #times, not n = #model_segments.  No references to self.anything.
        all_idx = np.arange(n)
        # output variables
        spincount = np.zeros(n)
        t_last = np.zeros(n)
        spinphase = np.zeros(n)
        spinper = np.zeros(n)
        eclipse_delta_phi = np.zeros(n)  # It is important that this variable is initialized to 0
        mask = np.zeros(n) + 3

        # Internal variables.
        # If memory becomes an issue, we can avoid allocating by using some creative index operations
        dt = np.zeros(n)
        fracspins = np.zeros(n)
        intspins = np.zeros(n, int)
        bp = np.zeros(n)
        phi_lastpulse = np.zeros(n)
        tlast_dt = np.zeros(n)

        idx1_cond = t < my_seg_times
        idx1 = all_idx[idx1_cond]
        c1 = len(idx1)

        idx2_cond = t > my_seg_t2
        idx2 = all_idx[idx2_cond]
        c2 = len(idx2)

        # each of the conditions below splits based on the truth of this subclause
        branch1_cond = np.abs(my_seg_c) < 1.0e-12
        branch1_idx = all_idx[branch1_cond]
        branch1_cidx = all_idx[~branch1_cond]
        branch1_c = len(branch1_idx)
        branch1_nc = len(branch1_cidx)
        tmp1 = np.bitwise_and(my_seg_segflags, 3)
        tmp2 = np.equal(tmp1, mask)
        tmp3 = np.greater(my_seg_idpu_spinper, 1.0)
        branch2_cond = tmp2 & tmp3
        branch2_idx = all_idx[branch2_cond]

        idx3_cond = (t >= my_seg_times) & (t <= my_seg_t2)
        idx3 = all_idx[idx3_cond]
        c3 = len(idx3)

        if c1 > 0:
            dt[idx1] = my_seg_times[idx1] - t[idx1]
            spinper[idx1] = 360.0 / my_seg_b[idx1]
            fracspins[idx1] = dt[idx1] / spinper[idx1]
            intspins[idx1] = np.ceil(fracspins[idx1])
            spinphase[idx1] = (intspins[idx1] - fracspins[idx1]) * 360.0
            spincount[idx1] = my_seg_c1[idx1] - intspins[idx1]
            t_last[idx1] = my_seg_times[idx1] - intspins[idx1] * spinper[idx1]

        if c2 > 0:
            dt[idx2] = t[idx2] - my_seg_t2[idx2]
            bp[idx2] = my_seg_b[idx2] + 2.0 * my_seg_c[idx2] * (my_seg_t2[idx2] - my_seg_times[idx2])
            spinper[idx2] = 360.0 / bp[idx2]
            fracspins[idx2] = dt[idx2] / spinper[idx2]

            idx2_branch_cond = idx2_cond & branch2_cond
            idx2_branch = all_idx[idx2_branch_cond]
            if len(idx2_branch) > 0:
                model_phi = fracspins[idx2_branch] * 360.0
                idpu_bp = 360.0 / my_seg_idpu_spinper[idx2_branch]
                idpu_phi = dt[idx2_branch] * idpu_bp
                eclipse_delta_phi[idx2_branch] = my_seg_initial_delta_phi[idx2_branch] + (model_phi - idpu_phi)
            intspins[idx2] = np.floor(fracspins[idx2])
            spinphase[idx2] = (fracspins[idx2] - intspins[idx2]) * 360.0
            spincount[idx2] = my_seg_c2[idx2] + intspins[idx2]
            t_last[idx2] = my_seg_t2[idx2] + intspins[idx2] * spinper[idx2]

        if c3 > 0:
            dt[idx3] = t[idx3] - my_seg_times[idx3]
            phi = my_seg_b[idx3] * dt[idx3] + my_seg_c[idx3] * dt[idx3] * dt[idx3]
            bp[idx3] = my_seg_b[idx3] + 2.0 * my_seg_c[idx3] * dt[idx3]
            spinper[idx3] = 360.0 / bp[idx3]
            spinphase[idx3] = np.fmod(phi, 360.0)
            fracspins[idx3] = phi / 360.0
            spincount[idx3] = np.floor(fracspins[idx3])
            phi_lastpulse[idx3] = spincount[idx3] * 360.0

            if branch1_c > 0:
                tlast_dt[branch1_idx] = phi_lastpulse[branch1_idx] / my_seg_b[branch1_idx]

            if branch1_nc > 0:
                tlast_dt[branch1_cidx] = (-my_seg_b[branch1_cidx] +
                                          np.sqrt(my_seg_b[branch1_cidx] ** 2 - 4.0 * my_seg_c[branch1_cidx] * (
                                              -phi_lastpulse[branch1_cidx]))) / (2.0 * my_seg_c[branch1_cidx])

            idx3_branch_cond = idx3_cond & branch2_cond
            idx3_branch = all_idx[idx3_branch_cond]

            if len(idx3_branch) > 0:
                model_phi = fracspins[idx3_branch] * 360.0
                idpu_bp = 360.0 / my_seg_idpu_spinper[idx3_branch]
                idpu_phi = dt[idx3_branch] * idpu_bp
                eclipse_delta_phi[idx3_branch] = my_seg_initial_delta_phi[idx3_branch] + (model_phi - idpu_phi)
            t_last[idx3] = my_seg_times[idx3] + tlast_dt[idx3]
            spincount[idx3] = spincount[idx3] + my_seg_c1[idx3]

        if use_spinphase_correction:
            logging.info("applying spinphase correction")
            interp_correction = np.interp(t, self.spin_corr_times, self.spin_corr_vals)
            spinphase -= interp_correction
            cond = spinphase > 360.0
            spinphase[cond] -= 360.0
            cond = spinphase < 0.0
            spinphase[cond] += 360.0

        res = SpinmodelInterpTResult(spincount=spincount, spinphase=spinphase, t_last=t_last,
                                     eclipse_delta_phi=eclipse_delta_phi, spinper=spinper, segflags=my_seg_segflags,
                                     idx=segs_idx, dt=dt)
        return res

    def make_arrays(self):
        """ Populate the seg_* attributes using data from the segment list

         For compatibility with the IDL implementation, we use the same algorithm in Python to build up a segment
         list from the STATE CDF variables.   In IDL, we can do vectorized access to class members through an array
         of indices, but this doesn't work the same way in Python.  Here, it is most convenient to convert the segment
         list to a set of Numpy arrays, which lets us do vectorized calculations on them.

         Args:

         Returns:
           """

        self.seg_count = len(self.seg_list)
        self.seg_times = np.array([o.t1 for o in self.seg_list])
        self.seg_t2 = np.array([o.t2 for o in self.seg_list])
        self.seg_c1 = np.array([o.c1 for o in self.seg_list])
        self.seg_c2 = np.array([o.c2 for o in self.seg_list])
        self.seg_b = np.array([o.b for o in self.seg_list])
        self.seg_c = np.array([o.c for o in self.seg_list])
        self.seg_npts = np.array([o.npts for o in self.seg_list])
        self.seg_maxgap = np.array([o.maxgap for o in self.seg_list])
        self.seg_phaserr = np.array([o.phaserr for o in self.seg_list])
        self.seg_idpu_spinper = np.array([o.idpu_spinper for o in self.seg_list])
        self.seg_initial_delta_phi = np.array([o.initial_delta_phi for o in self.seg_list])
        self.seg_segflags = np.array([o.segflags for o in self.seg_list])

    def make_tplot_vars(self,
                        prefix: str):
        """ Create a set of tplot variables from the spinmodel segment attributes.

        This is useful for regression testing or cross-platform validation of the spin model creation process.

        :param prefix : A string to prepend to each tplot variable name to ensure uniqueness
        :return:
        """

        store_data(prefix + 't1', data={'x': self.seg_times, 'y': self.seg_times})
        store_data(prefix + 't2', data={'x': self.seg_times, 'y': self.seg_t2})
        store_data(prefix + 'c1', data={'x': self.seg_times, 'y': self.seg_c1})
        store_data(prefix + 'c2', data={'x': self.seg_times, 'y': self.seg_c2})
        store_data(prefix + 'b', data={'x': self.seg_times, 'y': self.seg_b})
        store_data(prefix + 'c', data={'x': self.seg_times, 'y': self.seg_c})
        store_data(prefix + 'npts', data={'x': self.seg_times, 'y': self.seg_npts})
        store_data(prefix + 'maxgap', data={'x': self.seg_times, 'y': self.seg_maxgap})
        store_data(prefix + 'phaserr', data={'x': self.seg_times, 'y': self.seg_phaserr})
        store_data(prefix + 'idpu_spinper', data={'x': self.seg_times, 'y': self.seg_idpu_spinper})
        store_data(prefix + 'initial_delta_phi', data={'x': self.seg_times, 'y': self.seg_initial_delta_phi})
        store_data(prefix + 'segflags', data={'x': self.seg_times, 'y': self.seg_segflags})

    def addseg(self,
               newseg: SpinmodelSegment):
        """ Add a segment to the spin model object being constructed.

        A spin model is assumed to satisfy a condition that the end time of one segment exactly matches the start time
        of the next segment, with no gaps or overlaps.

        When loading STATE data for time intervals spanning multiple UTC days, there will be small time gaps
        between the spin model segments at either side of UTC date boundaries.  This routine adjusts the segment
        list by inserting new 'bridge' segments, as needed, to bridge gaps between the segments read from the CDF data,
        also making any necessary adjustments to the preceding/following segments.

        :param newseg: A SpinmodelSegment object to be added to the spin model being constructed
        :return:
        """

        if self.seg_count == 0:
            self.seg_list.append(newseg)
            self.lastseg = 0
            self.seg_count = 1
        else:
            lseg = self.seg_list[self.lastseg]
            # print('Adding segment')
            # print('Last:')
            # lseg.print()
            # print('Current')
            # newseg.print()
            # Previously, this was an exact equality test.  Now, the DEPEND_TIME variables are handled slightly
            # differently than plain old double-precision variables, so the possibility of small floating point
            # differences needs to be accounted for. For the purposes of spin model segments, if the times are within
            # a microsecond, they might as well be equal.
            tdiff = abs(newseg.t1 - lseg.t2)
            tolerance = 1.0e-06
            if tdiff < tolerance:

                #
                # Normal case: segments are contiguous
                #
                newseg.c1 = lseg.c2
                newseg.c2 = lseg.c2 + newseg.c2
                self.seg_list.append(newseg)
                self.lastseg += 1
                self.seg_count += 1
            else:
                # Segments are not contiguous -- this should indicate
                # a UTC date boundary, and the spin models on either side will
                # need to be merged.
                #
                # There are several cases, depending on the delta-t between the
                # end of the previous segment, and the start of the current segment:
                #
                # 1) Large gap, greater than 1/2 spin : create a new segment to
                #    bridge the gap.
                # 2) Small gap, <= 1/2 spin, previous segment covers 2 or more spins:
                #    remove last spin from previous segment, converting the situation
                #    to the "large gap" case, then create a new segment to bridge
                #    the gap.
                # 3) Small gap, previous segment only contains 1 spin : if current
                #    segment contains 2 or more spins, remove first spin from
                #    current segment, converting the situation to the "large gap"
                #    case, then create a new segment to bridge the gap.
                # 4) Small gap, previous and current segments each contain only
                #    a single spin.  This should never happen -- if no averaging
                #    was applied, the segments should be exactly contiguous.
                # 5) Negative gap -- current segment starts more than 1/2 spin
                #    before end of previous segment.  This should never happen,
                #    since it would imply that the apid 305 packets are incorrectly
                #    time ordered.

                spinper = 360.0 / lseg.b
                gap_spin_count = (newseg.t1 - lseg.t2) / spinper
                gap_time = newseg.t1 - lseg.t2
                if gap_spin_count > 0.5:
                    # Case 1: Gap of 1 or more spins between segments, add fill
                    gap_nspins = math.floor(gap_spin_count + 0.5)
                    gap_spinper = (newseg.t1 - lseg.t2) / (1.0 * gap_nspins)
                    # Fill in eclipse delta_phi parameters
                    gap_idpu_spinper = (newseg.idpu_spinper + lseg.idpu_spinper) / 2.0
                    gap_segflags = newseg.segflags & lseg.segflags
                    # We need to calculate gap_initial_delta_phi by extrapolating
                    # from lseg to lseg.t2 = gapseg.t1
                    spinper, spinphase, dummy_spincount, gap_eclipse_delta_phi, dummy_t_last = \
                        lseg.interp_t(lseg.t2)
                    fillseg = SpinmodelSegment(t1=lseg.t2, t2=newseg.t1, c1=lseg.c2, c2=lseg.c2 + gap_nspins,
                                               b=360.0 / gap_spinper, c=0.0, npts=0, maxgap=gap_time, phaserr=0.0,
                                               initial_delta_phi=gap_eclipse_delta_phi,
                                               idpu_spinper=gap_idpu_spinper, segflags=gap_segflags)
                    self.seg_list.append(fillseg)
                    self.lastseg = self.lastseg + 1
                    self.seg_count += 1
                    newseg.c1 = fillseg.c2
                    newseg.c2 = newseg.c1 + newseg.c2
                    self.seg_list.append(newseg)
                    self.lastseg = self.lastseg + 1
                    self.seg_count += 1
                elif gap_spin_count > -0.5:
                    # Case 2, 3, 4, or 5
                    # Now that we're using floating point time comparisons with tolerance, rather than strict
                    # equality, none of these cases seem to occur anymore. Cases 2 and (possibly) 3 have apparently
                    # been absorbed into the "segments are contiguous (within tolerance)" case.  Cases 4 and 5 were
                    # "this should never happen" scenarios.  It would be somewhat difficult to contrive plausible test
                    # inputs that would trigger cases 2 or 3 in this iteration of the code, so (for the sake of our test
                    # coverage metrics), I will replace those code blocks with exceptions. If they ever do turn up
                    # in practice, we can revive them from the version history or from the IDL code.  -- JWL 2023/03/13

                    if (lseg.c2 - lseg.c1) >= 2:
                        # Case 2: small gap, previous segment has at least 2 spins
                        # dprint,'<1 spin gap, stealing spin from last segment'
                        logging.error('Unexpected case 2 (small gap, previous segment with at least 2 spins)')
                        logging.error('Segment time: ' + time_string(lseg.t2))
                        logging.error('Please contact pyspedas or themis support and include the above information.')
                        raise RuntimeError
                    elif newseg.c2 >= 2:
                        # Case 3: small gap, previous segment has only 1 spin, current segment has at least 2 spins
                        # It is assumed that newseg is the first segment of a new UTC day, therefore the spin numbers
                        # start over at 0.  So we want to change newseg to start at spin 1 instead of spin 0.
                        logging.error('Unexpected case 3 (small gap, previous segment with only 1 spin, current segment with 2+ spins.)')
                        logging.error('Segment time: ' + time_string(lseg.t2))
                        logging.error('Please contact pyspedas or themis support and include the above information.')
                        raise RuntimeError
                    else:
                        # Case 4: small gap, but segments on either side only contain
                        # one spin each.  This should never happen.
                        logging.error('Unexpected case 4 (<1 spin gap, but neither segment has enough spins to steal.)')
                        logging.error('Segment time: ' + time_string(lseg.t2))
                        logging.error('Please contact pyspedas or themis support and include the above information.')
                        raise RuntimeError
                else:
                    # Case 5: out of order sun pulse times.  This should never happen.
                    logging.error('Unexpected case 5 (Sun pulse times out of order)')
                    logging.error("Last segment end time" + time_string(lseg.t2) + " New segment start time " + time_string(newseg.t1))
                    raise RuntimeError

    def get_timerange(self):
        """ Returns the time span covered by the model.
        The IDL version also returns information about any eclipse time periods, will add later
        if needed.

        Args: None

        Returns: tuple with start time and end time
        """
        start_time = self.seg_times[0]
        end_time = self.seg_t2[-1]
        return start_time, end_time

    def get_eclipse_times(self, min_shadow_duration:float=60.0):
        """ Returns lists of start time and end times for eclipses found in the spin model

        Args:
            None

        Returns: A tuple containing two listss, one for start times and one for end times.  Returns empty
            lists if no eclipses found.
        """
        start_times=[]
        end_times=[]
        processing_shadow=False

        for i in range(self.seg_count):
            this_eclipse_flag=self.seg_segflags[i] & 1
            if not(this_eclipse_flag) and not(processing_shadow):
                # Previous and current segments are not eclipses, do nothing
                pass
            elif not(this_eclipse_flag) and processing_shadow:
                # Transition out of shadow, reset status
                processing_shadow=False
            elif this_eclipse_flag and not(processing_shadow):
                # Transition into shadow, add entries to start and end time lists, set status
                start_times.append(self.seg_times[i])
                end_times.append(self.seg_t2[i])
                processing_shadow=True
            else:
                # Previous and current segments in shadow, update last end time
                end_times[-1]=self.seg_t2[i]

        return start_times, end_times





    def __init__(self,
                 probe,
                 correction_level,
                 suffix=''):
        self.lastseg = SpinmodelSegment(t1=0.0, t2=0.0, c1=0, c2=0, b=0.0, c=0.0, npts=0, maxgap=0.0, phaserr=0.0,
                                        initial_delta_phi=0.0, idpu_spinper=0.0, segflags=0)
        self.seg_times = np.zeros(1, float)
        self.seg_t2 = np.zeros(1, float)
        self.seg_c1 = np.zeros(1, int)
        self.seg_c2 = np.zeros(1, int)
        self.seg_b = np.zeros(1, float)
        self.seg_c = np.zeros(1, float)
        self.seg_npts = np.zeros(1, int)
        self.seg_maxgap = np.zeros(1, float)
        self.seg_phaserr = np.zeros(1, float)
        self.seg_initial_delta_phi = np.zeros(1, float)
        self.seg_idpu_spinper = np.zeros(1, float)
        self.seg_segflags = np.zeros(1, int)
        self.seg_count = 0
        self.seg_list = []
        seg_times, tend_data = get_sm_data(probe, 'tend', correction_level, suffix)
        _, spinper_data = get_sm_data(probe, 'spinper', correction_level, suffix)
        _, c_data = get_sm_data(probe, 'c', correction_level, suffix)
        _, phaserr_data = get_sm_data(probe, 'phaserr', correction_level, suffix)
        _, nspins_data = get_sm_data(probe, 'nspins', correction_level, suffix)
        _, npts_data = get_sm_data(probe, 'npts', correction_level, suffix)
        _, maxgap_data = get_sm_data(probe, 'maxgap', correction_level, suffix)
        _, initial_delta_phi_data = get_sm_data(probe, 'initial_delta_phi', correction_level, suffix)
        _, idpu_spinper_data = get_sm_data(probe, 'idpu_spinper', correction_level, suffix)
        _, segflags_data = get_sm_data(probe, 'segflags', correction_level, suffix)
        # The spin_correction variable only exists in V03 state CDFs, and has its own time variable
        tmp = get_sm_data(probe, 'correction', 0, suffix)
        if tmp is None:
            logging.info('spin_correction variable not available, defaulting to 0.0')
            self.spin_corr_times = [0.0, 1.0]
            self.spin_corr_vals = [0.0, 0.0]
        else:
            self.spin_corr_times, self.spin_corr_vals = tmp

        # The fgm_corr_offset and fgm_corr_tend variables may not exist, and have their own time variable
        tmp = get_sm_data(probe, 'fgm_corr_offset', correction_level, suffix)
        if tmp is None:
            do_fgm_corr = False
            logging.info('FGM correction variables not available')
        else:
            do_fgm_corr = True
            fgm_corr_time, fgm_corr_offset = tmp
            _, fgm_corr_tend = get_sm_data(probe, 'fgm_corr_tend', correction_level, suffix)

        seg_count = len(seg_times)
        # tlast = seg_times[0]
        for i in range(seg_count):
            newseg = SpinmodelSegment(t1=seg_times[i], t2=tend_data[i], c1=0, c2=nspins_data[i],
                                      b=360.0 / spinper_data[i],
                                      c=c_data[i], npts=npts_data[i], maxgap=maxgap_data[i], phaserr=phaserr_data[i],
                                      initial_delta_phi=initial_delta_phi_data[i], idpu_spinper=idpu_spinper_data[i],
                                      segflags=segflags_data[i])
            # tlast=tend_data[i]
            # origseg=copy.copy(newseg)
            self.addseg(newseg)
            # print(i)
            # newseg.print()
            # lastseg=copy.copy(origseg)
        self.make_arrays()
        if do_fgm_corr and (correction_level == 2):
            logging.info(f"applying FGM corrections, do_fgm_corr = {do_fgm_corr}, correction_level = {correction_level}")
            for i in np.arange(len(fgm_corr_offset)):
                self.adjust_delta_phi(fgm_corr_time[i], fgm_corr_tend[i], fgm_corr_offset[i])
        else:
            logging.info(f"Skipping FGM corrections, do_fgm_corr {do_fgm_corr}, correction_level = {correction_level}")


# This dictionary is where the spinmodel objects are stored.   The keys are tuples of (probe, correction_level)
# and the values are Spinmodel objects.  Spinmodel objects are added to the dictionary by the
# spinmodel_postprocess routine.

spinmodel_dict: Dict[(str, int)] = {}


def get_spinmodel(probe: str,
                  correction_level: int,
                  quiet: bool = False) -> Spinmodel:
    """ Get a reference to a Spinmodel object stored in the dictionary.

    Args:
        probe: Probe name, one of 'a','b','c','d','e'
        correction_level: 0 for no corrections, 1 for waveform corrections, 2 for spin fit corrections
        quiet:  If True, do not log anything if the model is uninitialized

    Returns:
        A reference to a Spinmodel object stored in the dictionary.
    """
    try:
        model = spinmodel_dict[(probe, correction_level)]
    except KeyError:
        if not quiet:
            logging.warning("No spinmodel loaded for probe " + probe + " correction level: " + str(correction_level))
            logging.warning("It is necessary to load THEMIS state data, with get_support_data=True, to initialize the spin model.")
        model = None
    return model


def save_spinmodel(probe: str,
                   correction_level: int,
                   model: Spinmodel):
    """ Store a reference to a Spinmodel object in the dictionary, using the probe and correction level as the key

    Args:
        probe: Probe name, one of 'a','b','c','d','e'
        correction_level: 0 for no corrections, 1 for waveform corrections, 2 for spin fit corrections
        model: A Spinmodel object to store

    """
    spinmodel_dict[(probe, correction_level)] = model
