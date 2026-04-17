"""Seed data for crm.create_opportunity_add_quotation_send.

Category: closed_loop_cross_module (HARD).
The agent must create a CRM opportunity from scratch, then use the
"New Quotation" smart button to create a linked sale order with exact
product lines, and finally send it via the email compose wizard.
"""

PARTNER_NAME = "Pinnacle Logistics Group"
PARTNER_EMAIL = "derek.voss@pinnacle-logistics.example.com"
DISTRACTOR_PARTNER = "Pinnacle Logistics Solutions"
DISTRACTOR_OPP = "Pinnacle Logistics Solutions - Fleet GPS"
PRODUCT_SPECS = [
    ("Warehouse Management Module", "service", 8500.0),
    ("Implementation Service", "service", 12000.0),
]


def setup(env):
    # --- Cleanup prior runs ---
    # Remove any quotations with target customer reference
    env["sale.order"].search([("client_order_ref", "=", "PLG-Q2-2026")]).unlink()

    # Remove opportunities created in prior runs
    prior_leads = env["crm.lead"].with_context(active_test=False).search([
        ("partner_id.name", "=", PARTNER_NAME),
    ])
    if prior_leads:
        # Remove linked quotations
        env["sale.order"].search([
            ("opportunity_id", "in", prior_leads.ids),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", prior_leads.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", prior_leads.ids),
        ]).unlink()
        prior_leads.unlink()

    # --- Partner ---
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "is_company": True,
            "email": PARTNER_EMAIL,
        })
    else:
        partner.write({
            "is_company": True,
            "email": PARTNER_EMAIL,
        })

    # --- Products ---
    for name, ptype, price in PRODUCT_SPECS:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            tmpl = env["product.template"].create({
                "name": name,
                "type": ptype,
                "list_price": price,
                "invoice_policy": "order",
                "taxes_id": [(5, 0, 0)],
            })
        else:
            product.product_tmpl_id.write({
                "list_price": price,
                "type": ptype,
                "invoice_policy": "order",
                "taxes_id": [(5, 0, 0)],
            })

    # --- Distractor: similar-named company and opportunity ---
    distractor_partner = env["res.partner"].search(
        [("name", "=", DISTRACTOR_PARTNER)], limit=1
    )
    if not distractor_partner:
        distractor_partner = env["res.partner"].create({
            "name": DISTRACTOR_PARTNER,
            "is_company": True,
            "email": "info@pinnacle-solutions.example.com",
        })

    distractor_opp = env["crm.lead"].search(
        [("name", "=", DISTRACTOR_OPP)], limit=1
    )
    if not distractor_opp:
        stage = env["crm.stage"].search(
            [("name", "=", "New"), ("is_won", "=", False)], limit=1
        )
        if not stage:
            stage = env["crm.stage"].search([], order="sequence", limit=1)
        admin = env.ref("base.user_admin")
        env["crm.lead"].create({
            "name": DISTRACTOR_OPP,
            "type": "opportunity",
            "partner_id": distractor_partner.id,
            "user_id": admin.id,
            "stage_id": stage.id if stage else False,
            "expected_revenue": 18000.0,
        })
