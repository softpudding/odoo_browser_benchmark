# Cookbook notes — appointment.public_booking_reschedule_cancel_portal

## Module availability audit: appointment in Odoo Community

`appointment` appears in `ir_module_module` as
`state='uninstallable'` on the `odoo_benchmark` branch because the
module is enterprise-only and no source code is vendored under
`addons/`.  `button_immediate_install()` raises `UserError` on
uninstallable records.

### Implications for task authors

- Any `appointment.*` task that depends on `appointment.type`,
  `appointment.resource`, `appointment.booking_line`, or the public
  `/appointment/<slug>` controllers is non-buildable on this branch.
- `calendar.event` cannot substitute cleanly: the only public-portal
  calendar surface is `/calendar/meeting/view` (Accept/Decline
  buttons only — no Reschedule, no Cancel exposed).
- Before allocating new `appointment.*` tasks to the backlog, verify
  with:
  ```sql
  SELECT name, state FROM ir_module_module WHERE name LIKE 'appointment%';
  ```
  If any row shows `uninstallable`, the task is blocked until the
  enterprise addon is vendored.

## Pattern for BLOCKED-task commits

When a backlog task is provably unbuildable in the current repo state
(missing addon, missing data, etc.), still commit a skeleton directory
with:

1. `task.yaml` carrying `metadata.blocked_reason` and
   `primary_track: false`.
2. `seed.py` / `oracle.py` / `check.py` that short-circuit with clear
   diagnostic `RuntimeError` messages rather than silently passing.
3. `expected_state.json = []` and `state_spec.yaml: models: {}`.
4. A `RESULT.md` recording the blocker evidence + re-enabling
   instructions.
5. STATUS.md row set to `Removed` with `FAIL (module unavailable)` in
   the oracle column, plus a detailed section at the end.

This keeps the backlog tidy (future agents don't try to re-pick the
same task) while preserving the original intent for when the
constraint is lifted.

## Precedent

See `appointment.portal_reschedule_and_cancel_booking` (already in
STATUS.md as Removed) for an identical blocker from an earlier batch.
