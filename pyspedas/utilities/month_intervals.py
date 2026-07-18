from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import TypeAlias

import numpy as np
from numpy.typing import NDArray


FloatArray: TypeAlias = NDArray[np.float64]


def month_intervals(
    start_time: float,
    end_time: float,
    *,
    boundary_tolerance: float = 1.0e-6,
) -> FloatArray:
    """Return complete calendar-month intervals covering a Unix-time range.

    Each returned interval uses half-open semantics::

        [month_start, next_month_start)

    Parameters
    ----------
    start_time
        Beginning of the requested interval, as a Unix timestamp.

    end_time
        End of the requested interval, as a Unix timestamp. It must be
        greater than or equal to ``start_time``.

    boundary_tolerance
        Absolute tolerance, in seconds, used when deciding whether
        ``end_time`` falls exactly on a calendar-month boundary.

    Returns
    -------
    numpy.ndarray
        An array with shape ``(n_months, 2)``. Each row contains the Unix
        timestamps for the beginning of a month and the beginning of the
        following month.

    Notes
    -----
    If ``end_time`` falls exactly on a month boundary, the month beginning
    at ``end_time`` is not included, unless ``start_time == end_time``.

    Examples
    --------
    >>> from datetime import datetime, timezone
    >>> start = datetime(2024, 1, 15, 12, tzinfo=timezone.utc).timestamp()
    >>> end = datetime(2024, 4, 1, tzinfo=timezone.utc).timestamp()
    >>> intervals = month_intervals(start, end)
    >>> [
    ...     (
    ...         datetime.fromtimestamp(t0, tzinfo=timezone.utc).isoformat(),
    ...         datetime.fromtimestamp(t1, tzinfo=timezone.utc).isoformat(),
    ...     )
    ...     for t0, t1 in intervals
    ... ]
    [('2024-01-01T00:00:00+00:00', '2024-02-01T00:00:00+00:00'),
     ('2024-02-01T00:00:00+00:00', '2024-03-01T00:00:00+00:00'),
     ('2024-03-01T00:00:00+00:00', '2024-04-01T00:00:00+00:00')]
    """
    start_time = float(start_time)
    end_time = float(end_time)

    if not math.isfinite(start_time):
        raise ValueError("start_time must be a finite Unix timestamp")

    if not math.isfinite(end_time):
        raise ValueError("end_time must be a finite Unix timestamp")

    if end_time < start_time:
        raise ValueError("end_time must be greater than or equal to start_time")

    start_datetime = datetime.fromtimestamp(start_time, tz=timezone.utc)
    end_datetime = datetime.fromtimestamp(end_time, tz=timezone.utc)

    first_month = _month_start(start_datetime)
    end_month = _month_start(end_datetime)

    end_is_month_boundary = math.isclose(
        end_time,
        end_month.timestamp(),
        rel_tol=0.0,
        abs_tol=boundary_tolerance,
    )

    if end_is_month_boundary and end_time > start_time:
        exclusive_end = end_month
    else:
        exclusive_end = _next_month(end_month)

    intervals: list[tuple[float, float]] = []
    current_month = first_month

    while current_month < exclusive_end:
        following_month = _next_month(current_month)

        intervals.append(
            (
                current_month.timestamp(),
                following_month.timestamp(),
            )
        )

        current_month = following_month

    return np.asarray(intervals, dtype=np.float64)


def _month_start(value: datetime) -> datetime:
    """Return the beginning of the calendar month containing value."""
    return datetime(value.year, value.month, 1, tzinfo=timezone.utc)


def _next_month(value: datetime) -> datetime:
    """Return the beginning of the calendar month following value."""
    if value.month == 12:
        return datetime(value.year + 1, 1, 1, tzinfo=timezone.utc)

    return datetime(value.year, value.month + 1, 1, tzinfo=timezone.utc)