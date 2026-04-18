# stock_barcode.receive_via_barcode_scan_validate — RESULT

## Verdict: REMOVED (module unavailable — Enterprise-only)

This task is blocked because the `stock_barcode` addon is an **Odoo
Enterprise** module that is not vendored in this Odoo 19 Community
codebase. The Barcode tablet UI at `/odoo/barcode` (receipts / internal
transfers / deliveries scanning screen with scan input, `+ 1` quantity
button, and Validate tile) ships entirely inside `stock_barcode`.

## Evidence

Inspected `addons/` on branch `odoo_benchmark`:

```
$ ls addons/ | grep -iE "barcode|stock_bar"
barcodes
barcodes_gs1_nomenclature

$ grep -rn "stock_barcode" addons/ | head
addons/stock/models/res_config_settings.py:29:
    module_stock_barcode = fields.Boolean("Barcode Scanner")
addons/stock/models/res_config_settings.py:30:
    module_stock_barcode_barcodelookup = fields.Boolean("Stock Barcode Database")
addons/mrp/views/res_config_settings_views.xml:36:
    <field name="module_stock_barcode" widget="upgrade_boolean"/>
# plus i18n po strings only
```

Key findings:

- Only the `barcodes` addon (keyboard-event mixin + nomenclature
  resolver) and `barcodes_gs1_nomenclature` are present. These provide
  USB-scanner keystroke capture but NO warehouse receipt / picking
  scanning UI.
- `module_stock_barcode` on `stock.res.config.settings` is an
  `upgrade_boolean` — ticking it in the UI asks Odoo to install the
  (absent) `stock_barcode` module and fails.
- There is no `/odoo/barcode` controller, no `stock_barcode_action_main_menu`
  client action, no `BarcodePickingModel` JS class, no `receipt_line.js`,
  no `BarcodeMainMenu` component in this codebase.
- The same precedent task `barcodes.receive_product_via_scan_validate`
  (STATUS.md section ~2425) was Removed for the same reason.

The task's central step ("open `/odoo/barcode`, scan BENCH-A-001 three
times, tap Validate") therefore cannot be executed — there is no such
screen in Community. Seeding the `stock.picking` + products would
succeed technically, but the agent would land on a 404 when navigating
to the Barcode app.

## Precedent

Tasks Removed on the same grounds (Enterprise-only addon / feature
missing in Community):

- `barcodes.receive_product_via_scan_validate` — same `stock_barcode`
  absence, earlier attempt.
- `appointment.public_booking_reschedule_cancel_portal` (row 350) —
  appointment module uninstallable.
- `helpdesk.team_sla_assign_escalate_close` (row 351) — helpdesk module
  absent.
- `marketing_automation.tag_trigger_drip_campaign` (row 352) —
  marketing_automation absent.
- `hr_skills_survey.link_certification_survey_to_skill` (row 387) —
  `hr.skill.survey_id` Enterprise-only.

All use the same BLOCKED-skeleton pattern: short-circuit seed / oracle /
check with diagnostic errors, ship empty `expected_state.json` +
`state_spec: {}` + `trace_spec: []`, STATUS row set to Removed with
`FAIL (module unavailable)`.

## Lifecycle status

- Pre-flight: FAILED — `ls addons/stock_barcode/` returned
  "No such file or directory".
- Oracle: did NOT run (short-circuits with RuntimeError).
- BU: did NOT run.
- F1: N/A.
- Calibration: N/A.

## Re-enabling

To re-enable, vendor the enterprise `stock_barcode` addon (plus any
compatible `stock_barcode_*` siblings) into `addons/`. Then:

1. Replace the `raise RuntimeError` / `raise NotImplementedError` guards
   in `seed.py` with the real seed (sketch is already in the comment
   block at the bottom of `seed.py`).
2. Flesh out `oracle.py` with the three-phase flow documented in the
   module docstring. Verify selector names against the current
   enterprise Barcode app (`o_barcode_input`, `.o_add_reserved`, or
   their current equivalents).
3. Flesh out `check.py` to assert `stock.picking` named
   `R-BENCH-BC-001` is `state=='done'` with exactly two `stock.move`
   rows, each `quantity==3.0`, and no backorder.
4. Populate `state_spec.yaml` + `expected_state.json` from a real run's
   `state_diff.json`.
5. Flip STATUS row 401 from Removed → WIP and re-run the normal
   lifecycle.
