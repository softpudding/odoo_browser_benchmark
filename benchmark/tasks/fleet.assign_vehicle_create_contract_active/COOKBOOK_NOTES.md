# Cookbook notes — fleet.assign_vehicle_create_contract_active

New quirks observed while building this task. Promoted to
`benchmark/ODOO19_PATTERNS.md § Fleet`.

## 1. `fleet.vehicle.log.contract` has NO "Activate Contract" header button

- The form header in `fleet_vehicle_log_contract_view_form` contains ONLY
  `<field name="state" widget="statusbar" options="{'clickable': '1'}"/>`.
- There is no `<button name="action_open"/>` (or "Activate") exposed in
  the form header. The model has `action_open()` / `action_draft()` /
  `action_close()` / `action_expire()` Python methods, but they are only
  wired to the clickable statusbar widget, not to visible header buttons.
- Tasks that say "click Activate Contract" must be rephrased to "click
  the **Running** step on the statusbar".

## 2. Default `state='open'` on fresh create; `write()` hook is a no-op for create

- The model default is `state='open'` (see
  `addons/fleet/models/fleet_vehicle_log_contract.py` line 52).
- The `write()` override flips state to `futur` when `start_date > today`
  (and to `open` / `expired` otherwise), BUT it runs on `write()` only,
  not on `create()`.
- Consequence: a contract created through the UI with a future
  `start_date` still lands in `state='open'` (Running), NOT `'futur'`
  (New). There is no way to land a fresh-created contract in draft via
  the UI alone.
- Tasks that want a "draft → activate" lifecycle must pre-seed an
  existing contract in seed.py via
  `contract.write({'state': 'futur'})` or `contract.action_draft()`.
- Tasks that just confirm Running must tolerate the idempotent case:
  the statusbar's current step renders as
  `<button disabled aria-current="step" data-value="open">`, and a
  Playwright click on a disabled button times out.

## 3. Oracle pattern for "click Running if not already current"

```python
running_locator = page.locator(
    ".o_statusbar_status button[data-value='open']:visible"
).first
already_open = False
try:
    if running_locator.get_attribute("aria-current") == "step":
        already_open = True
except Exception:
    already_open = False

if not already_open:
    running_locator.click()
```

## 4. `cost_subtype_id` ("Type") autocomplete requires `category='contract'`

- Shared table `fleet.service.type` with service costs (which use
  `category='service'`). The contract form filters with
  `domain=[('category', '=', 'contract')]`.
- Seed must create the type with `category='contract'` or autocomplete
  returns nothing.

## 5. `insurer_id` is the Vendor field on contract

- Labeled "Vendor" on the form, m2o to `res.partner`,
  `widget="many2one_avatar"`. Standard `set_many2one` helper works.
- Distinct from `vendor_id` on `fleet.vehicle.log.services` — do not
  cross-reference field names between the two log models.

## 6. Driver partner: use `create(... driver_id=partner_id)` not post-create write

- `fleet.vehicle.write({'driver_id': ...})` auto-creates an
  `fleet.vehicle.assignation.log` row (existing ODOO19_PATTERNS quirk).
- Passing `driver_id` directly to `create()` captures the log once at
  seed time with `date_start=today`. Cleanup removes the log alongside
  the vehicle.
