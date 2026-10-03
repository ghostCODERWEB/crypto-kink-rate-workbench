"""Evaluate piecewise borrow rates and reserve-adjusted supply yields across utilization scenarios."""

from .common import (
    number,
    integer,
    identity,
    records,
    chronology,
    allocate,
    result,
    validate_document,
)
from decimal import Decimal


def _analyze(d):
    base = number(d["base"])
    s1 = number(d["slope_low"])
    s2 = number(d["slope_high"])
    kink = number(d["kink"], maximum=1)
    reserve = number(d["reserve_factor"], maximum=1)
    if kink == 0 or kink == 1:
        raise ValueError("kink strictly inside unit interval")
    rows = []
    for value in d["utilizations"]:
        u = number(value, maximum=1)
        borrow = (
            base + s1 * u / kink
            if u <= kink
            else base + s1 + s2 * (u - kink) / (1 - kink)
        )
        rows.append(
            {
                "utilization": u,
                "borrow_apr": borrow,
                "supply_apr": borrow * u * (1 - reserve),
                "reserve_apr": borrow * u * reserve,
            }
        )
    return result(
        {"curve": rows, "rate_at_kink": base + s1, "maximum_rate": base + s1 + s2}
    )


def analyze(document):
    validate_document(document)
    try:
        return result(_analyze(document))
    except (KeyError, TypeError, ArithmeticError, RecursionError) as error:
        raise ValueError("invalid domain input: " + str(error)) from error
