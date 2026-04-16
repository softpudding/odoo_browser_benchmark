"""Seed three similar-named CRM opportunities.

Category 2 (MEDIUM): The agent must pick the right opportunity among two
distractors, update expected_revenue, and click the status-bar Won button.
"""


OPPORTUNITIES = [
    # (name, stage_name, expected_revenue)
    ("Crestline Networks - Managed VPN", "Qualified", 40000.0),
    ("Crestline Networks - Firewall Expansion", "New", 25000.0),
    ("Crestline Retail - POS Refresh", "Proposition", 18000.0),
]


def setup(env):
    refs = [o[0] for o in OPPORTUNITIES]

    # Cleanup prior runs (including archived/won)
    prior = env["crm.lead"].with_context(active_test=False).search(
        [("name", "in", refs)]
    )
    if prior:
        env["mail.message"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", prior.ids),
        ]).unlink()
        prior.unlink()

    partner = env["res.partner"].search([("name", "=", "Crestline Networks")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Crestline Networks",
            "email": "ops@crestline-networks.example.com",
        })
    retail = env["res.partner"].search([("name", "=", "Crestline Retail")], limit=1)
    if not retail:
        retail = env["res.partner"].create({
            "name": "Crestline Retail",
            "email": "buyer@crestline-retail.example.com",
        })

    partner_by_name = {
        "Crestline Networks - Managed VPN": partner,
        "Crestline Networks - Firewall Expansion": partner,
        "Crestline Retail - POS Refresh": retail,
    }

    admin = env.ref("base.user_admin")

    for name, stage_name, revenue in OPPORTUNITIES:
        stage = env["crm.stage"].search([("name", "=", stage_name), ("is_won", "=", False)], limit=1)
        if not stage:
            stage = env["crm.stage"].search([("name", "=", stage_name)], limit=1)
        env["crm.lead"].create({
            "name": name,
            "type": "opportunity",
            "partner_id": partner_by_name[name].id,
            "user_id": admin.id,
            "stage_id": stage.id if stage else False,
            "expected_revenue": revenue,
            "probability": 40.0,
        })
