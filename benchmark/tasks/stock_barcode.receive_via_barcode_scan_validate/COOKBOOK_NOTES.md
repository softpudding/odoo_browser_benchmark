# Cookbook notes — stock_barcode.receive_via_barcode_scan_validate

## Feature availability audit: stock_barcode in Community

Odoo 19 Community ships only two barcode-related addons:

1. `addons/barcodes/` — provides:
   - `barcode_events_mixin.BarcodeEventsMixin` — keyboard-event handler
     that captures Enter-terminated key bursts from USB scanners and
     broadcasts `barcode_scanned` bus events.
   - `barcode.nomenclature` / `barcode.rule` models for GS1-style
     prefix parsing.
   - `res.config.settings.module_barcode` and a dashboard hook — but NO
     warehouse receipt / picking UI.
2. `addons/barcodes_gs1_nomenclature/` — GS1 Application-Identifier
   parser extension (dates, lots, weights).

The actual warehouse scanning experience — the `/odoo/barcode` route,
the Operations / Inventory Adjustments / Batch Transfers main menu, the
tablet UI with scan input + `+ 1` button + Validate tile, the
`BarcodePickingModel` / `BarcodeMainMenu` / `LineComponent` JS classes,
and the `stock.picking` integration that mass-scans and auto-routes — is
**Enterprise-only** (`stock_barcode` + optional siblings
`stock_barcode_barcodelookup`, `stock_barcode_quality_control`,
`stock_barcode_mrp`).

`grep -rn "stock_barcode" addons/` on the `odoo_benchmark` branch
returns only i18n po strings and one boolean in
`addons/stock/models/res_config_settings.py`:

```python
module_stock_barcode = fields.Boolean("Barcode Scanner")
module_stock_barcode_barcodelookup = fields.Boolean("Stock Barcode Database")
```

These are `upgrade_boolean` fields — ticking them in Inventory Settings
asks Odoo to install the absent module, which fails with "Module not
found".

### Implications for task authors

- Any task that requires the agent to open `/odoo/barcode`, use the
  scan input, or tap the `+ 1`/Validate tiles is **not buildable** on
  Community.
- A workflow-adjacent task ("process a stock.picking through the
  backend list/form view") IS possible in Community — file it under
  `stock.*` without the `stock_barcode.` prefix.
- Before picking any `stock_barcode.*` task (scan-to-receive,
  scan-to-pack, cycle-count via scan, batch transfer via scan,
  cluster picking, etc.), confirm with:
  ```python
  module = env["ir.module.module"].search(
      [("name", "=", "stock_barcode")], limit=1)
  bool(module) and module.state == "installed"
  ```
  If False, the task is blocked until the enterprise addon is vendored.

## Pattern for BLOCKED-task commits (reminder)

Following the precedent set by `appointment.public_booking_reschedule_cancel_portal`,
`helpdesk.team_sla_assign_escalate_close`,
`marketing_automation.tag_trigger_drip_campaign`,
`hr_skills_survey.link_certification_survey_to_skill`, and the earlier
`barcodes.receive_product_via_scan_validate`, BLOCKED tasks ship:

1. `task.yaml` with `metadata.blocked_reason` + `primary_track: false` +
   `version: "0.0-blocked"`.
2. `seed.py` / `oracle.py` / `check.py` that short-circuit with clear
   diagnostic `RuntimeError` / list-of-failures messages rather than
   silently passing. Each file should also carry a *commented* sketch
   of the real body so a future agent has a starting point once the
   constraint is lifted.
3. `expected_state.json = []` and `state_spec.yaml: models: {}` and
   empty `trace_spec` lists.
4. A `RESULT.md` recording the blocker evidence + re-enabling steps.
5. STATUS.md row set to `Removed` with `FAIL (module unavailable)` in
   the oracle column, plus a detailed section at the end.

## Precedent

- `barcodes.receive_product_via_scan_validate` — nearly identical
  shape, removed for identical reason.
- `appointment.public_booking_reschedule_cancel_portal` (row 350)
- `helpdesk.team_sla_assign_escalate_close` (row 351)
- `marketing_automation.tag_trigger_drip_campaign` (row 352)
- `hr_skills_survey.link_certification_survey_to_skill` (row 387)

All five (including this task) share the same core shape:
Enterprise-only feature / addon absent in Community, skeleton preserved
for forward compatibility.
