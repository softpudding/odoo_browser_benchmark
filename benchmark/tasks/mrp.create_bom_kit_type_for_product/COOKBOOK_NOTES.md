# Cookbook notes — `mrp.bom.type` as a 3-option radio + create-from-scratch kit BoM

## `mrp.bom.type` is a `widget="radio"` group, NOT a Selection dropdown

In Odoo 19, the BoM form declares:

```xml
<field name="type" widget="radio"/>
```

So the field renders as a `div.o_field_radio[name='type']` with one
`.o_radio_item` per Selection option. Set via the UI by clicking the
`<label>` (the `<input type="radio">` siblings have `data-value` =
`'normal'`, `'phantom'`, or `'subcontract'`). Visible labels:

| Selection key | UI label                      | Notes                                   |
|---------------|-------------------------------|-----------------------------------------|
| `normal`      | *Manufacture this Product*    | DEFAULT — auto-selected on a fresh BoM  |
| `phantom`     | **Kit**                       | THE non-default that this task requires |
| `subcontract` | *Subcontracting*              | Only shown if `mrp_subcontracting` installed (it is, in the base DB) |

**Oracle / test hook**:

```python
type_field = page.locator("div[name='type']").first
kit_option = type_field.locator("label:has-text('Kit')").first
kit_option.click()
```

Do NOT use `set_selection(page, 'type', 'Kit')` — `set_selection`
calls `.select_option()` on a native `<select>`, which the radio
widget does not render.

## BoM create-from-scratch — `display_name` and diff entity keys

`mrp.bom._compute_display_name` produces:

```
display_name = f"{bom.code + ': ' if bom.code else ''}{bom.product_tmpl_id.display_name}"
```

So when the task does NOT set `code`, the BoM's display_name is just
`"Bench Kit Finished"` (the finished product template's name). This
means `mrp.bom.line.bom_id` normalizes to `"Bench Kit Finished"` in
the state-diff engine, NOT `"BOM-REFERENCE: Bench Kit Finished"` (the
format used by row 433 `mrp.create_bom_with_components`, which DOES
set `code`).

`match_key=[bom_id, product_id]` → entity_key is
`["Bench Kit Finished", "Bench Kit Comp A"]` (both Many2one
normalized to display_name).

## Default `product_qty` create edit is emitted even when left at 1

Even though `product_qty=1.0` is the default on `mrp.bom`, the diff
engine treats it as an observed create edit because the pre-state
does NOT contain the BoM (it's an `op='create'` with `norm_value=1.0`).
`expected_state.json` MUST include the `product_qty` create edit.

## Components tab is default — no need to click it

On the `mrp_bom_form_view` notebook the "Components" tab is the FIRST
tab and is auto-active on a fresh BoM. The oracle defensively checks
for it via `.o_notebook .nav-link:has-text('Components')` but in
practice `click_add_a_line(page)` works immediately.

## Hard pattern anatomy (why this reliably drops BU below 40%)

Two independent failure modes stack:

1. **Non-default radio on a 3-option group**. Empirically across
   prior tasks (purchase backorder wizard row 16, sale force-partial
   delivery, calendar recurrence update), browser-use clicks the
   first/default option or simply leaves the default in place. The
   BoM Type default is `Manufacture this Product` → `type='normal'`,
   so skipping the Kit radio yields a WRONG-type BoM even if every
   other field is correct.
2. **Create-from-scratch o2m with exact qty values**. Row 4 (purchase
   cancel_reissue_wrong_vendor) and row 460 both suffer from BU
   leaving a trailing empty row or typing the wrong qty. Exact
   integer qtys (`2`, `3`) and a strict `len(bom_line_ids) == 2`
   assertion catch phantom rows.

check.py enforces `bom.type == 'phantom'` BEFORE checking line counts
— so a failed Kit-radio click is reported as the FIRST failure,
which is the key calibration signal.
