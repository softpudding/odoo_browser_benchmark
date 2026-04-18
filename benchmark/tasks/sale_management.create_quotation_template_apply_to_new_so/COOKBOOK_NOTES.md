# Cookbook notes from sale_management.create_quotation_template_apply_to_new_so

## `sale_management.group_sale_order_template` gates two UI surfaces

The `sale_management.group_sale_order_template` feature group (toggled
from Sales Settings as **"Quotation Templates"**) gates BOTH:

1. The **Sales > Configuration > Quotation Templates** menu (xmlid
   `sale_management.sale_order_template_menu`).
2. The **Quotation Template** `sale_order_template_id` field on the
   `sale.order` form (attribute
   `groups="sale_management.group_sale_order_template"` on the inherited
   view `sale_management.sale_order_form_quote`).

Seeds that want the agent to immediately see both surfaces must
`group.sudo().write({"user_ids": [(4, admin.id)]})` in `seed.py`.
Granting only one surface (e.g. setting the Sales config param) is not
enough — the group itself is the gate.

Direct action URL for the templates list:
`/odoo/action-sale_management.sale_order_template_action`.

## `sale.order.template` line edit uses `so_template_line_o2m` (editable list)

The Lines tab on `sale.order.template` uses the custom
`so_template_line_o2m` widget (a `SectionAndNoteListRenderer` extension),
but the underlying list view is still `<list editable="bottom">`. Standard
`click_add_a_line` + `set_o2m_many2one(row, "product_id", ...)` +
`set_o2m_field(row, "product_uom_qty", ...)` works without any special
handling. Note the field on the list is `product_id` (NOT
`product_template_id` like the `sale.order` form's `sol_o2m` widget).

## `sale.order.sale_order_template_id` auto-populates order lines via onchange

Setting `sale_order_template_id` on a new `sale.order` fires the
`_onchange_sale_order_template_id` hook which **clears** existing
`order_line` and **creates** one `sale.order.line` per template line via
`sale.order.template.line._prepare_order_line_values()`. Net effect for
the agent: picking the template in the m2o is a single interaction that
populates the full lines section — no line-by-line data entry needed.

The field uses `options="{'no_create': True}"`, so the autocomplete will
NOT offer a quick-create branch; the template must already exist (hence
the two-stage workflow). The field is also `readonly="state in
['cancel', 'sale']"`, so it must be set while the SO is still in draft.

## `sale.order.template.name` renders as the H1 title (field name `name`)

The template form wraps `<field name="name" ...>` inside the `oe_title`
H1 block. `fill_field(page, "name", "...")` targets
`.o_field_widget[name='name'] input` and works — do NOT use an `h1 input`
selector.

## State-diff `sale.order.template` match_key: `[name]` is stable

The template has no `state` / status lifecycle (just `active`), and
`name` is required + unique enough for the diff engine. `match_key:
[name]` works cleanly. Include `active=true` in `expected_state.json`
because the diff engine emits `op: "create"` with `norm_value: true` for
the default-True `active` field on any newly-created template.

## `sale.order.sale_order_template_id` normalizes to the template name (no currency suffix)

Unlike `product.pricelist.display_name` (which appends ` (USD)` etc.),
`sale.order.template.display_name` is just `name`. expected_state.json
entry for the SO's `sale_order_template_id` uses the bare string
`"Bench Starter Pack"`.
