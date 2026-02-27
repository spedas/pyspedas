import numpy as np
from scipy.integrate import solve_ivp
from .refactored_gp_interface import make_rhs_direction, make_event_br_zero

R_E_KM = 6371.2

def trace_to_event(model, startpos_re, *,
                   event: str,
                   direction: float = 1.0,
                   max_s: float = 200.0,
                   max_step: float = 0.05,
                   rtol: float = 1e-6,
                   atol: float = 1e-9,
                   # ionosphere options
                   r_iono_re: float = 6468.4 / R_E_KM,
                   # equator options
                   s_min_event: float = 0.1,
                   br_direction: float = 0.0):
    """
    Trace a magnetic field line using dx/ds = direction * B/|B| and stop on an event.

    Parameters
    ----------
    model:
        Object with method B_gsm(pos_re)->(3,) array (nT). (IGRF + external as desired)
    startpos_re:
        Initial position (3,) in Earth radii.
    direction: float
        1.0 to trace parallel to the B vector, -1.0 for anti-parallel
    event:
        "iono" or "equator"
    max_s:
        Max path length in Re before giving up.
    max_step:
        Max RK45 step in Re.
    rtol, atol:
        Integrator tolerances (position units are Re).
    r_iono_re:
        Ionosphere radius in Re (used if event="iono").
    s_min_event:
        Don't allow equator event triggering before this path length (used if event="equator").
    br_direction:
        Event crossing direction for Br=0. 0.0 means accept either crossing.

    Returns
    -------
    pts : (N,3) array
        Trace points (includes interpolated event point if reached).
    status : str
        "iono" / "equator" if event reached, else "max_s" (or "bad_B" if B undefined early).
    sol : OdeResult
        Raw SciPy solution.
    """

    startpos_re = np.asarray(startpos_re, dtype=float)
    """
    # RHS: geometry-only tracing
    def rhs(s, pos):
        B = np.asarray(model.B_gsm(pos), dtype=float)
        n = np.linalg.norm(B)
        if not np.isfinite(n) or n == 0.0:
            # Returning zeros will stall; solve_ivp will keep stepping but not move.
            # For QA, it's often better to just stall and let max_s stop it,
            # or you can raise an exception instead.
            return np.zeros(3)
        return direction * (B / n)
    """
    model_rhs = make_rhs_direction(model, direction=direction)

    # Choose event
    if event == "iono":
        def evt(s, pos):
            return np.linalg.norm(pos) - r_iono_re
        evt.terminal = True
        evt.direction = -1.0  # typically moving inward toward smaller radius

    elif event == "equator":
        evt = make_event_br_zero(model_rhs, s_min_event=s_min_event)
        """
        def evt(s, pos):
            if s < s_min_event:
                return 1.0
            r = np.linalg.norm(pos)
            if r == 0.0:
                return 1.0
            rhat = pos / r
            B = np.asarray(model_rhs(s, pos), dtype=float)
            return float(np.dot(B, rhat))  # Br
        evt.terminal = True
        evt.direction = br_direction
        """

    else:
        raise ValueError('event must be "iono" or "equator"')

    sol = solve_ivp(
        fun=model_rhs,
        t_span=(0.0, max_s),
        y0=startpos_re,
        method="RK45",
        max_step=max_step,
        rtol=rtol,
        atol=atol,
        events=[evt],
        dense_output=True,
    )

    pts = sol.y.T  # accepted steps

    reached = (sol.t_events[0].size > 0)
    if reached:
        s_event = sol.t_events[0][0]
        pts = np.vstack([pts, sol.sol(s_event)])
        status = event
    else:
        status = "max_s"

    return pts, status, sol