# Kinked interest rate workbench: domain model

Evaluate piecewise borrow rates and reserve-adjusted supply yields across utilization scenarios.

## Input contract

| Field | Example JSON shape |
|---|---|
| `base` | `str` |
| `slope_low` | `str` |
| `slope_high` | `str` |
| `kink` | `str` |
| `reserve_factor` | `str` |
| `utilizations` | `list` |

The fixture includes nested records and concrete units. Engine validation is authoritative: required keys are read explicitly, identifiers must be nonempty, integer amounts reject booleans, record IDs are unique where indicated, and chronological logs reject reversed timestamps. A document is bounded to 100,000 values, depth 25 and 10,000 entries per collection. Domain-specific tighter bounds apply where required. Extra fields are tolerated and ignored.

## Calculation and outputs

The domain function executes on supplied data without mutation. Results include intermediate allocations, traces or per-scenario records so aggregate outputs can be reconciled. Four known-answer assertions in `tests/test_domain.py` cover the example independently of the generated regression output. Inspect `cryptolab/engine.py` for the executable algorithm and explicit rejection paths.

## Explicit assumptions

APR is a declared synthetic curve, not a forecast or fetched protocol rate. No compounding or interest settlement.

Input correctness and completeness remain the caller's responsibility. Offline results are educational and cannot prove external account ownership, protocol safety, source authenticity or future outcomes. Decimal precision follows Python's default 28 significant digits. Do not use illustrative fixture numbers as market data.
