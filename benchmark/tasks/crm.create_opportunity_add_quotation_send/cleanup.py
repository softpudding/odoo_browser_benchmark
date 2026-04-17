"""Clean up artifacts from previous runs."""

PARTNER_NAME = "Pinnacle Logistics Group"
DISTRACTOR_OPP = "Pinnacle Logistics Solutions - Fleet GPS"
DISTRACTOR_PARTNER = "Pinnacle Logistics Solutions"
CUSTOMER_REF = "PLG-Q2-2026"


def cleanup(env):
    # Remove quotations by customer ref
    env["sale.order"].search([("client_order_ref", "=", CUSTOMER_REF)]).unlink()

    # Remove opportunities and linked quotations for target partner
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        leads = env["crm.lead"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        if leads:
            env["sale.order"].search([
                ("opportunity_id", "in", leads.ids),
            ]).unlink()
            env["mail.message"].search([
                ("model", "=", "crm.lead"),
                ("res_id", "in", leads.ids),
            ]).unlink()
            env["mail.activity"].search([
                ("res_model", "=", "crm.lead"),
                ("res_id", "in", leads.ids),
            ]).unlink()
            leads.unlink()

    # Remove distractor opportunity
    distractor = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", DISTRACTOR_OPP),
    ])
    if distractor:
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", distractor.ids),
        ]).unlink()
        distractor.unlink()

    # Remove distractor partner
    env["res.partner"].search([("name", "=", DISTRACTOR_PARTNER)]).unlink()
