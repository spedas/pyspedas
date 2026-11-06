"""Add the GOES X-ray flare class scale to tplot panels."""

import logging
from math import isfinite, sqrt

from pyspedas.tplot_tools import annotate, databar, get_data, options, tplot_wildcard_expand

logger = logging.getLogger(__name__)

_BOUNDARIES = (1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3)  # Flux in W/m^2; the last boundary marks X10.
_TAG = "_goes_xray_annotations"  # Identify decorations owned by this helper.


def add_goes_xray_annotations(tvars, yrange=None, color=None, fontsize=10):
    """Add horizontal boundaries and A/B/C/M/X labels to X-ray flux panels.

    Parameters
    ----------
    tvars : str or list of str
        Tplot variable names or wildcard patterns. Combined variables
        (pseudovariables) are supported. Select panels containing 1-8 Angstrom
        X-ray irradiance in W/m^2, such as GOES-R ``xrsb_flux``. Names and units
        are not checked, and data are not converted.
    yrange : sequence of float, optional
        Positive, increasing y limits. By default, preserve the current range.
        Use ``[1e-8, 1e-3]`` to display all five labels. Logarithmic y scaling
        is enabled in either case.
    color : str or color specification, optional
        Color for the labels and horizontal lines. By default, labels use the
        global foreground color (or black), and lines are gray.
    fontsize : float or str, optional
        Label font size in points or a Matplotlib size name. Default is 10.

    Returns
    -------
    list of str
        Variables annotated. Returns an empty list if no suitable variables
        match. Non-time-varying variables are skipped with a warning.

    Raises
    ------
    ValueError
        If ``yrange`` does not contain two finite, positive, increasing limits.

    Notes
    -----
    The class thresholds are A: 1e-8, B: 1e-7, C: 1e-6, M: 1e-5 and
    X: 1e-4 W/m^2 in the 1-8 Angstrom band. Labels sit at the logarithmic
    midpoint of each decade, at the panel's right edge. Labels
    outside the visible range are clipped. The line at 1e-3 W/m^2 marks X10;
    it is not an upper limit on X-class flares.

    Existing annotations and bars are preserved. Repeated calls replace only
    decorations added by this helper. For panels with separate left and right
    y axes, the decorations use the left axis. Call ``tplot`` after applying
    the helper to draw the updated panel. Component decorations also appear
    when overplotted, so apply the helper once to the combined panel.

    See https://www.swpc.noaa.gov/phenomena/solar-flares-radio-blackouts
    for the NOAA flare classification.

    Examples
    --------
    >>> from pyspedas import tplot
    >>> from pyspedas.projects import goes
    >>> names = goes.xrs(probe="18", trange=["2023-01-01", "2023-01-02"])
    >>> goes.add_goes_xray_annotations("g18_xrs_xrsb_flux", yrange=[1e-8, 1e-3])
    >>> tplot("g18_xrs_xrsb_flux")

    Alternatively, load the data and annotate a combined panel once, after
    creating it:

    >>> from pyspedas import store_data
    >>> names = goes.xrs(probe="18", trange=["2023-01-01", "2023-01-02"])
    >>> store_data("combined_xrs", data=["g18_xrs_xrsa_flux", "g18_xrs_xrsb_flux"])
    >>> goes.add_goes_xray_annotations("combined_xrs", yrange=[1e-8, 1e-3])
    >>> tplot("combined_xrs")
    """
    # Require exactly two finite, positive, increasing limits for the log axis.
    if yrange is not None:
        try:
            lower, upper = (float(limit) for limit in yrange)
        except (TypeError, ValueError) as exc:
            raise ValueError("yrange must contain two finite, positive, increasing limits") from exc
        if not (0 < lower < upper and isfinite(upper)):
            raise ValueError("yrange must contain two finite, positive, increasing limits")
        yrange = [lower, upper]

    # Resolve names and wildcard patterns; report an empty match once below.
    names = tplot_wildcard_expand(tvars, quiet=True)
    if not names:
        logger.warning("No valid tplot variables specified for GOES X-ray annotations")
        return []

    annotated = []
    for name in names:
        # Work with stored plot metadata; skip variables without plotting options.
        metadata = get_data(name, metadata=True)
        if not isinstance(metadata, dict) or "plot_options" not in metadata:
            logger.warning("Skipping non-time-varying variable %s", name)
            continue
        plot_options = metadata["plot_options"]
        # Replace only this helper's earlier labels and bars, preserving other decorations.
        annotations = plot_options.get("extras", {}).get("annotations") or []
        options(name, "annotations", [item for item in annotations if not item.get(_TAG)])
        plot_options["time_bar"] = [item for item in plot_options.get("time_bar") or [] if not item.get(_TAG)]

        # Enable log scaling, retaining the existing limits unless new ones were supplied.
        options(name, "ylog", True)
        if yrange is not None:
            options(name, "yrange", yrange)

        # Tag only the newly appended horizontal bars so later calls can replace them.
        bar_start = len(plot_options["time_bar"])
        databar(name, list(_BOUNDARIES), color=color if color is not None else "gray", dash=True)
        for bar in plot_options["time_bar"][bar_start:]:
            bar[_TAG] = True
        # Each geometric mean is the center of a decade on the logarithmic axis.
        for label, lower, upper in zip("ABCMX", _BOUNDARIES[:-1], _BOUNDARIES[1:]):
            annotate(
                name,
                label,
                (1.0, sqrt(lower * upper)),
                xycoords=("axes fraction", "data"),  # Anchor x at the right edge and y at the flux value.
                color=color,
                fontsize=str(fontsize),
                annotation_clip=True,  # Hide labels whose anchor falls outside the visible panel.
            )
            # annotate() appends one entry; mark it for replacement on the next call.
            plot_options["extras"]["annotations"][-1][_TAG] = True
        annotated.append(name)

    return annotated
