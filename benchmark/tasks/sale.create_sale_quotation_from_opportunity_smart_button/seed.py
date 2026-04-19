"""Seed for sale.create_sale_quotation_from_opportunity_smart_button.

Category: cross_module_handoff / smart-button create (MEDIUM).

Sets up:
- A `Bench Opp Co` partner (customer) used as the opportunity's partner_id.
- A consu product `Bench Opp Product` (list_price=100.0, taxes cleared) so
  line price_unit is deterministic for the post-check (100.00 @ qty=2).
- A `crm.lead` of `type='opportunity'` named `Bench Opp Sale` with
  partner=`Bench Opp Co`, stage=first non-won, expected_revenue=10000 and no
  linked quotations yet. Agent must use the Quotations smart button
  (`action_view_sale_quotation`, widget=statinfo on field `quotation_count`)
  to create a new sale.order — the smart-button action pre-fills
  `default_opportunity_id` via `_prepare_opportunity_quotation_context`.
"""

OPP_NAME = "Bench Opp Sale"
PARTNER_NAME = "Bench Opp Co"
PARTNER_EMAIL = "ops@benchoppco.example.com"
PRODUCT_NAME = "Bench Opp Product"
EXPECTED_REVENUE = 10000.0


def setup(env):
    # --- Cleanup any sale.orders tied to prior opportunity / partner ---
    old_partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if old_partner:
        old_orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", old_partner.id),
        ])
        for order in old_orders:
            if order.state == "sale":
                order.action_cancel()
            order.sudo().unlink()

    # --- Cleanup prior opportunity (deletes linked messages/activities) ---
    old_leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    if old_leads:
        # Remove any remaining sale orders by opportunity_id before removing the lead
        so_by_opp = env["sale.order"].with_context(active_test=False).search([
            ("opportunity_id", "in", old_leads.ids),
        ])
        for order in so_by_opp:
            if order.state == "sale":
                order.action_cancel()
            order.sudo().unlink()

        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", old_leads.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", old_leads.ids),
        ]).unlink()
        old_leads.unlink()

    # --- Cleanup prior product ---
    old_product = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if old_product:
        old_product.mapped("product_tmpl_id").sudo().unlink()

    # --- Partner ---
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "is_company": True,
            "email": PARTNER_EMAIL,
        })

    # --- Product: consu, list_price=100, no taxes (clean math 100 * 2 = 200) ---
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "list_price": 100.0,
        "taxes_id": [(5, 0, 0)],
    })
    product = tmpl.product_variant_id
    product.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]

    # --- Pick a sensible starting stage (first non-won) ---
    first_stage = env["crm.stage"].search(
        [("is_won", "=", False)], order="sequence asc, id asc", limit=1
    )
    if not first_stage:
        first_stage = env["crm.stage"].search([], order="sequence asc, id asc", limit=1)

    # --- Create the opportunity ---
    env["crm.lead"].create({
        "name": OPP_NAME,
        "type": "opportunity",
        "partner_id": partner.id,
        "email_from": PARTNER_EMAIL,
        "stage_id": first_stage.id if first_stage else False,
        "expected_revenue": EXPECTED_REVENUE,
        "probability": 20.0,
        "description": "Ready to quote via Quotations smart button.",
    })
