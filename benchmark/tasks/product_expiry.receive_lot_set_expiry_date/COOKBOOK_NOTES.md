# Cookbook notes — product_expiry.receive_lot_set_expiry_date

## product_expiry is NOT in base snapshot

Seed must install it on demand:

```python
mod = env["ir.module.module"].search(
    [("name", "=", "product_expiry")], limit=1
)
if mod and mod.state != "installed":
    mod.button_immediate_install()
```

Depends only on `stock`. Adds `use_expiration_date` / `expiration_time`
/ `use_time` / `removal_time` / `alert_time` (Integer days) to
`product.template`, and `expiration_date`/`use_date`/`removal_date`/
`alert_date` (Datetime) + `use_expiration_date` (Boolean,related) to
`stock.lot`.

## stock.lot.expiration_date widget is a <button>, not an <input>

`addons/web/static/src/views/fields/datetime/datetime_field.xml` renders
the DateTimeField as a **`<button class="o_input">`** whenever the
field has a value AND is not the active picker input. Clicking the
button flips it into an editable `<input>`. Playwright selectors that
only target `.o_field_widget[name='X'] input` time out on the button
render path.

Correct pattern for setting a datetime field inside a dialog:

```python
widget = dialog.locator(f".o_field_widget[name='{name}']").first
widget.scroll_into_view_if_needed()
widget.locator("button, input").first.click()  # flip to input
page.wait_for_timeout(400)
inp = widget.locator("input").first
inp.wait_for(state="visible", timeout=5000)
inp.fill("")
inp.type("04/17/2026 00:00:00", delay=20)
page.keyboard.press("Escape")           # close picker popover
dialog.locator(".modal-title").click()  # commit
```

This also applies to any stock.lot form opened inline (readonly-looking
date fields are just un-activated buttons).

## stock.lot from Detailed Operations popup → nested dialog

Clicking the internal-link arrow (`.o_external_button`) on the
`lot_id` m2o inside the Detailed Operations popup does NOT navigate —
`openRecord('dialog')` is chosen because `env.inDialog=True`
(`many2one.xml` line 35). Result: a **second** stack of `.modal:visible`
appears, with the stock.lot form rendered inline.

- Multiple `.modal:visible` selectors: `modals.last` is the lot dialog,
  but it's safer to walk the visible modals and pick the one that
  contains `.o_field_widget[name='expiration_date']` (stock.lot
  fingerprint) — the search popup can briefly elevate other modals.
- The lot dialog renders `display_complete=True` automatically because
  the lot has been persisted (its `id` is truthy).
- The save button footer reads **"Save"** (with a Discard sibling) —
  not "Save & Close" — on this nested form.

## stock.lot expiration_date / removal_date interaction

`_compute_dates` on `stock.lot` recomputes `use_date`, `removal_date`,
and `alert_date` every time `expiration_date` changes. The logic:

```python
if lot.expiration_date and not lot._origin.expiration_date:
    # initial creation — derive from template
    use_date = expiration_date - timedelta(days=product_tmpl.use_time)
    removal_date = expiration_date - timedelta(days=product_tmpl.removal_time)
    alert_date = expiration_date - timedelta(days=product_tmpl.alert_time)
elif lot._origin.expiration_date:
    # changing expiration_date — shift the others by the delta
    time_delta = lot.expiration_date - lot._origin.expiration_date
    use_date = lot._origin.use_date + time_delta
    ...
```

Consequence: on the nested dialog you **must set `expiration_date`
first**, then `removal_date` — otherwise writing `removal_date` first
gets clobbered by the `expiration_date` onchange compute. The oracle
explicitly writes in that order.

## Receipts picking type: use_create_lots + use_existing_lots

- `use_create_lots=True` alone → popup shows `lot_name` (text-only)
  column; NO internal-link button → NO path to the stock.lot form for
  setting expiration_date.
- `use_existing_lots=True` alone → popup shows `lot_id` (m2o) column
  but no autocomplete **Create** option → cannot create on the fly.
- **Both True** → popup shows `lot_id` (m2o) with Create autocomplete
  + internal-link button = the desired flow for this task.

The `show_lots_m2o`/`show_lots_text` compute on `stock.move` gates
which column is visible. Seed must set both flags True.
