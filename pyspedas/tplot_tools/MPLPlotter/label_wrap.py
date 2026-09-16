"""Helpers for axis label composition used by the MPLPlotter tplot renderer.

This module is intentionally dependency-free (only :mod:`textwrap`) so it can
be unit-tested without pulling in matplotlib or the full ``pyspedas``
package init chain. It is imported by ``tplot.py`` for the ``xwrap``/``ywrap``
options introduced in issue #1444.
"""
import textwrap


def wrap_label(label, width=40):
    """Wrap a multi-line axis label to the given character width.

    Whitespace-only wrap with ``break_long_words=False`` and
    ``break_on_hyphens=False`` so scientific notation (``1e-6``, ``m/s^2``),
    subscripts (``x_1``), and LaTeX fragments (``$cm^{-3}$``) survive intact.

    Empty/short strings pass through unchanged. Newlines embedded in the
    input are preserved as hard breaks; each line segment is wrapped
    independently and rejoined with ``"\\n"``.

    Parameters
    ----------
    label: str
        The composed label (typically ``xtitle + '\\n' + xsubtitle`` or the
        equivalent for the y-axis).
    width: int, optional
        Maximum line length in characters. Default: ``40``.

    Returns
    -------
    str
        The wrapped label, ready to pass to ``Axes.set_xlabel`` /
        ``Axes.set_ylabel``.
    """
    if not label:
        return label
    parts = label.split("\n")
    wrapped = [
        textwrap.fill(
            p.strip(),
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        )
        if p.strip()
        else ""
        for p in parts
    ]
    return "\n".join(wrapped)


# Backwards-compatible alias for the in-tplot.py helper that preceded the
# extraction. The ``_`` prefix matches the original symbol so callers in
# ``tplot.py`` keep working unchanged.
_wrap_label = wrap_label
