# fleet.log_service_cost_add_odometer_close — Run Result

## Oracle

- Wall clock: 41.2s
- Steps: 0 (synchronous)
- Success: True
- StateDiffF1: 1.0 (8/8 edits matched)
- Postconditions: PASS
- API trace: 45 calls (21 writes, 24 reads), required-op recall 1.0, 0 forbidden writes.

Oracle script creates the service record, fills odometer on the same form
(which auto-materialises the `fleet.vehicle.odometer` log via the `odometer`
inverse), saves, and then clicks the clickable-statusbar `Done` button.

## Browser-Use (single shot, 270.7s)

- Wall clock: 270.7s
- Success: False
- StateDiffF1: 0.0 (Precision 0.0 / Recall 0.0)
- Matching edits: 7 / 8 expected; 29 unexpected extras.
- Postcondition failures:
  - Expected exactly 1 service record for 'BENCH-TRUCK-01', found **4**.
  - Vendor is not set.
  - Expected exactly 1 odometer log for 'BENCH-TRUCK-01', found **6**
    (values = `[25000.0, 0.0025, 0.0025, 0.0025, 25000.0, 25000.0]`).

## Failure mode (as intended for hard tier)

Browser-use spiralled into a multi-create loop:

1. Attempted the odometer entry with a **thousands separator (`25,000`)**,
   which Odoo's numeric widget parsed as `0.0025` (comma treated as
   decimal-point by the ECMAScript `Intl.NumberFormat` admin-locale fallback).
   This produced three phantom odometer logs at value `0.0025`.
2. After save, clicked `New` again — the save-on-a-new-form pattern — and
   re-typed the same service fields, producing four duplicate
   `fleet.vehicle.log.services` records. Three of them missed the vendor
   because BU tried to retype it as plain text instead of picking from
   autocomplete.
3. Eventually clicked the correct `Done` statusbar button on the 4th record
   (state diff shows 3 additional `state=done` transitions), but count
   postconditions gated F1 to 0.0.

This matches the predicted failure pattern: **odometer-field skip/duplicate +
thousands-separator parse + multi-record spawn**.
