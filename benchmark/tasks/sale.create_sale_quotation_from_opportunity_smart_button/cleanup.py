"""Cleanup for sale.create_sale_quotation_from_opportunity_smart_button.

Reverses seed.py and any records the agent may have created:
- Deletes the sale.order linked to opportunity 'Bench Opp Sale' and any
  sale.order for 'Bench Opp Co'.
- Deletes the opportunity lead and its messages/activities.
- Deletes the product template.
- Deletes the partner.
"""

OPP_NAME = "Bench Opp Sale"
PARTNER_NAME = "Bench Opp Co"
PRODUCT_NAME = "Bench Opp Product"


def cleanup(env):
    # --- sale.orders by opportunity (may be created by the agent) ---
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    if leads:
        orders_by_opp = env["sale.order"].with_context(active_test=False).search([
            ("opportunity_id", "in", leads.ids),
        ])
        for order in orders_by_opp:
            if order.state == "sale":
                order.action_cancel()
            order.sudo().unlink()

    # --- sale.orders by partner (catches orders created without opp link) ---
    partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        orders_by_partner = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        for order in orders_by_partner:
            if order.state == "sale":
                order.action_cancel()
            order.sudo().unlink()

    # --- Remove opportunity and its chatter ---
    if leads:
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        leads.unlink()

    # --- Remove product ---
    product = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if product:
        product.mapped("product_tmpl_id").sudo().unlink()

    # --- Remove partner ---
    if partner:
        partner.sudo().unlink()
