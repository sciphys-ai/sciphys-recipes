# Recipe: Battery Health Screening

## Scientific Question

Given battery tester time-series data, what early signals suggest capacity fade,
internal resistance increase, or abnormal cycling behavior?

## Inputs

- Voltage, current, time, cycle index, capacity, and temperature when available.
- Instrument metadata and cell chemistry if known.

## Workflow

1. Parse the tester export.
2. Normalize units and align cycle boundaries.
3. Compute capacity retention, coulombic efficiency, resistance proxy, and
   abnormal voltage response.
4. Compare the current cell against historical cells or public demo baselines.
5. Produce an interpretable health summary with evidence.

## Evidence Examples

- capacity retention trend;
- charge/discharge asymmetry;
- voltage plateau drift;
- abnormal temperature response;
- cycle-to-cycle instability.

## Expert Feedback

Experts should be able to label:

- normal aging;
- early degradation;
- measurement artifact;
- safety concern;
- needs repeat test.
