# Cookbook notes from building maintenance.create_equipment_schedule_preventive_plan

## Non-existent fields in the task spec — `next_action_date`
The original task row 373 spec asked for `next_action_date=2026-06-01` on
`maintenance.equipment`. That field **does not exist** on the model in Odoo 19
(only referenced in a handful of translation `.po` files; no Python / XML
uses it). Writable date fields on `maintenance.equipment` are:
`effective_date`, `warranty_date`, `assign_date`, `scrap_date`, plus the
computed `estimated_next_failure` / `latest_failure_date` (readonly).
Substituted `effective_date` — it is the default-today, writable start date
used by the MTBF computation, which matches the preventive-plan semantics.

## Two-phase save is a reliable BU failure mode
"Save the form, then reopen and set one more field" consistently causes
browser-use to create a duplicate record instead of re-editing the saved
one. In this run BU produced two `Bench Press 01` equipment records and two
`Machinery` categories. Good medium-tier trap that does not require any
wizard — just two discrete save phases.

## `expected_mtbf` vs `mtbf`
Already documented in ODOO19_PATTERNS, confirmed again here: `expected_mtbf`
is the writable Integer; `mtbf` is a `_compute_maintenance_request`
field (readonly). Prompt must reference **Expected Mean Time Between
Failure** exactly.

## Category cleanup guard
`maintenance.equipment.category._unlink_except_contains_maintenance_requests`
prevents deletion while equipment or requests reference it. Seed must delete
prior equipment **first**, then attempt category unlink with a guard:
```python
for cat in stale_cats:
    if not cat.equipment_ids and not cat.maintenance_ids:
        cat.unlink()
```
