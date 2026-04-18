# Cookbook notes — fleet.log_service_cost_add_odometer_close

New quirks observed while building this task. Worth promoting to
`benchmark/ODOO19_PATTERNS.md` if they recur.

## 1. `fleet.vehicle.log.services.odometer` is a **computed Float with an inverse**

- `odometer` is a Float (not a m2o), and its inverse `_set_odometer` creates a
  new `fleet.vehicle.odometer` row linked to the same `vehicle_id` with
  `value = odometer` and `date = log.date or today()`.
- Consequence: filling the Odometer Value field on the service form is
  **sufficient** to satisfy "add an odometer reading". The agent does NOT
  need to open the Odometers list manually. Oracle relies on this — only
  one `fleet.vehicle.odometer` row is created end-to-end.
- Guard: `if odometer == 0: del data['odometer']` in `create()` short-circuits
  the inverse, so zero-value fills are silently dropped. Prompts that want an
  odometer log MUST specify a non-zero target.

## 2. `fleet.vehicle.log.services.state` is a clickable statusbar

- Declared `widget="statusbar" options="{'clickable': '1'}"`.
- Values: `new / running / done / cancelled` (there is no separate kanban
  state or stage model — `state` IS the stage).
- Click target: `.o_statusbar_status button.o_arrow_button:has-text('Done')`
  (the standard clickable-statusbar pattern, same as `project.task.stage_id`).
- Unlike header action-buttons, no confirmation dialog — click persists
  immediately and Odoo autosaves.

## 3. Browser-use decimal-separator trap: `25,000` → `0.0025`

- Typing the literal string `25,000` into the Odometer numeric input
  (monetary-less Float widget) causes Odoo's JS locale parser to treat the
  comma as a **decimal point** (admin default locale is `en_US` but Owl's
  `parseFloat` helper normalises commas too). Result: `value = 0.0025`.
- Seen in this task: BU created **three** phantom odometer rows at 0.0025
  before eventually typing the value without comma.
- Mitigation for future tasks: phrase the prompt as "25000" WITHOUT a
  thousands separator OR explicitly forbid commas. This task keeps the
  bare-numeric phrasing on purpose — the comma parse is part of the
  hard-tier calibration.

## 4. Monetary widget locks to `company.currency_id`

- `fleet.vehicle.log.services.currency_id` is `related='company_id.currency_id'`.
- To have the "Cost" field render with an EUR symbol, seed must flip
  `env.company.currency_id` to EUR (and activate the currency if
  `active=False`, which is the default in a fresh base snapshot). Writing
  `currency_id` directly on the service record raises `AttributeError` — it's
  a related readonly field.

## 5. `driver_id` auto-creates an assignation log — use `create()` not `write()`

- Known (already in ODOO19_PATTERNS.md § Fleet), but worth restating: seeding
  the vehicle via `create({..., 'driver_id': admin.partner_id.id})` captures
  the assignation log at seed time with `date_start=today`. Using a post-
  create `write({'driver_id': ...})` achieves the same log, but splitting
  seed into create + write makes the order-of-operations around task timing
  brittle — keep it in `create()`.

## 6. State spec — odometer match_key must include `value`

- `fleet.vehicle.odometer` has `vehicle_id` + `value` + `date`. Matching only
  on `vehicle_id` would collapse all odometer rows for a vehicle into one
  entity_key, hiding the BU phantom-row problem. Using
  `match_key: [vehicle_id, value]` gives the diff engine a row per unique
  value, which is exactly what we want for the miscount assertion.
