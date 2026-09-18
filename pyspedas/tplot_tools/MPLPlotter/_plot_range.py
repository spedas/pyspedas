"""Set plot limits without changing an axis's current direction."""


def set_axis_range(axis, limits, dimension):
    """Apply coordinate-ordered limits while preserving axis inversion."""
    if dimension == "x":
        axis.set_xlim(limits[::-1] if axis.xaxis_inverted() else limits)
    else:
        axis.set_ylim(limits[::-1] if axis.yaxis_inverted() else limits)
