# Cookbook notes from purchase.set_vendor_product_code_on_po_line

## The `name` (Description) column on purchase.order.line is FOLDED into `product_id`

On the PO form, the order_line list uses
`widget="product_label_section_and_note_field_o2m"` with inner
`widget="product_label_section_and_note_field"` on `product_id`.
`ProductNameAndDescriptionListRendererMixin.getActiveColumns()`
(addons/product/static/src/product_name_and_description/product_name_and_description.js:20-38)
DELETES the standalone `name` column from the active column list
when both `product_id` and `name` columns are declared, and sets
`record.columnIsProductAndLabel = true`. The description editor
moves into the SAME `<td name='product_id'>` cell as the product
Many2One.

Consequence: `td[name='name']` does NOT exist in the DOM for the
inline list. Trying to click it with `set_o2m_field(page, 0, 'name',
...)` or `td[name='name']` selectors will time out.

## The description textarea is HIDDEN until a toggler is clicked

The widget's template
(addons/account/static/src/components/product_label_section_and_note_field/product_label_section_and_note_field.xml:49-58)
renders the description `<textarea>` with `class="d-none"` whenever
`!(columnIsProductAndLabel and (label or labelVisibility.value))` is
true. Since the `label` getter (product_name_and_description.js:107-113)
strips the product display name prefix and returns `""` when
`name == product_name`, a freshly-seeded line with no custom
description starts with the textarea hidden.

A toggler button is rendered in that case:
```html
<button id="labelVisibilityButtonId" class="btn fa fa-bars ..."
        data-tooltip="Click or press enter to add a description"/>
```
Clicking it sets `labelVisibility.value = true` and the textarea
un-hides.

Oracle locator for the toggler:
```python
selected_row.locator(
    "td[name='product_id'] button.o_external_button.fa-bars, "
    "td[name='product_id'] button.fa-bars, "
    "td[name='product_id'] button[data-tooltip*='description']"
).first
```

Fallback: strip the `d-none` class in JS if the toggler is flaky.

## `parseLabel` prepends `productName + "\n"` to typed text

`ProductLabelSectionAndNoteField.parseLabel`
(product_label_section_and_note_field.js:50-54):
```js
parseLabel(value) {
    return (this.productName && value && this.productName.concat("\n", value))
        || (this.productName && !value && this.productName)
        || (value || "");
}
```

Typing `BENCH-WDG-A1 / Bench Widget` into the label yields a stored
`name` of **`"Bench Widget\nBENCH-WDG-A1 / Bench Widget"`** — two
lines separated by `\n`. You CANNOT get a single-line stored value
through this widget; the product name prefix is unavoidable.

If your task requires an exact single-line `name`, the agent must
open the line's **sub-form** (via the row form-view chevron or the
Edit on a line-form popup) where `<field name="name"/>` renders as a
plain textarea without label stripping. The default PO view does NOT
expose an "Open in form view" chevron (`hasOpenFormViewButton` is
false); double-clicking the row in editable-bottom mode opens the
inline editor, not the sub-form.

Cookbook rule: expected_state.json norm_value for description edits
via the inline widget MUST include the `productName + "\n"` prefix.

## entity_key on purchase.order.line is `[null, null]`

With `match_key: [order_id, product_id]` both normalize to null in
the state diff — `purchase.order.line.order_id` normalizes to null
here, NOT to the PO name (unlike `sale.order.line.order_id`, which
normalizes to the SO name per the row-440 sibling task). Use
`entity_key: [null, null]` in expected_state.json. If there are
multiple lines on the PO, the diff engine will tag duplicates as
`[null, null, "#dup1"]`, `[null, null, "#dup2"]`, etc.

## Forbidden ops list should catch delete-and-recreate

Include in `trace_spec.yaml`:
```yaml
forbidden_ops:
  - purchase.order.line.create
  - purchase.order.line.unlink
  - purchase.order.button_confirm
  - purchase.order.button_cancel
```
An agent that deletes the line and recreates it with a new name
trips `purchase.order.line.create`/`.unlink`. One that accidentally
clicks "Confirm Order" trips `button_confirm`.

## Calibration: single-shot pass — too easy for medium

BU solved single-shot in 72.6s / 9 steps because the prompt tells
the agent to click the `.fa-bars` toggler explicitly. To harden the
task: remove the hint about the toggler, or require a description
that does NOT contain the product name (forcing the sub-form path).
