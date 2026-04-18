"""Seed for sale_management.create_quotation_template_apply_to_new_so.

Category: deep_ui_interaction (MEDIUM).

The agent must create a sale.order.template ('Bench Starter Pack') with two
product lines (Bench Widget x5, Bench Gadget x2), save it, and then create a
new sale.order for customer 'Bench Test Co' that uses the template so the
two lines auto-populate via the _onchange_sale_order_template_id hook.

Seeded state:
- `sale.group_sale_order_template` feature group enabled on the admin user
  so that Sales > Configuration > Quotation Templates menu + the Quotation
  Template field on the SO form are both visible.
- Two consumable products with no taxes (clean math):
    * Bench Widget  list_price = 10.0
    * Bench Gadget  list_price = 20.0
- Customer 'Bench Test Co' (no pricelist / no special config).
- Cleanup removes prior runs including the template, any SO created by a
  previous agent run, the products, and the partner.
"""

PARTNER_NAME = "Bench Test Co"
TEMPLATE_NAME = "Bench Starter Pack"
PRODUCT_WIDGET = "Bench Widget"
PRODUCT_GADGET = "Bench Gadget"


def setup(env):
    admin = env.ref("base.user_admin")

    # --- Enable the Quotation Templates feature group on admin ---
    # Gates: (a) Sales > Configuration > Quotation Templates menu,
    # (b) `sale_order_template_id` field on sale.order form.
    tmpl_group = env.ref("sale_management.group_sale_order_template")
    tmpl_group.sudo().write({"user_ids": [(4, admin.id)]})

    # --- Cleanup child-first ---
    partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        old_orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        for order in old_orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            order.sudo().unlink()

    # Remove any SOs that reference our target template (in case the template
    # still exists from a prior failed run).
    old_template = env["sale.order.template"].with_context(active_test=False).search(
        [("name", "=", TEMPLATE_NAME)]
    )
    if old_template:
        orphan_orders = env["sale.order"].with_context(active_test=False).search([
            ("sale_order_template_id", "in", old_template.ids),
        ])
        for order in orphan_orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            order.sudo().unlink()
        old_template.sudo().unlink()

    for pname in (PRODUCT_WIDGET, PRODUCT_GADGET):
        old_product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if old_product:
            old_product.mapped("product_tmpl_id").sudo().unlink()

    if partner:
        partner.sudo().unlink()

    # --- Create products (no taxes → clean state-diff) ---
    widget_tmpl = env["product.template"].create({
        "name": PRODUCT_WIDGET,
        "type": "consu",
        "list_price": 10.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    widget_tmpl.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]

    gadget_tmpl = env["product.template"].create({
        "name": PRODUCT_GADGET,
        "type": "consu",
        "list_price": 20.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    gadget_tmpl.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]

    # --- Create customer ---
    env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "bench.test@example.com",
    })
