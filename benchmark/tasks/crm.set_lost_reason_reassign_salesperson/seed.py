"""Seed for crm.set_lost_reason_reassign_salesperson."""

OPP_NAME = "Acme – Q3 renewal"
LOST_REASON = "Too expensive"


def setup(env):
    admin = env.ref("base.user_admin")

    # Cleanup prior runs.
    env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ]).unlink()

    # Ensure the lost reason exists.
    reason = env["crm.lost.reason"].with_context(active_test=False).search([
        ("name", "=", LOST_REASON),
    ], limit=1)
    if not reason:
        reason = env["crm.lost.reason"].create({"name": LOST_REASON})
    elif not reason.active:
        reason.write({"active": True})

    # Partner for the opportunity.
    partner = env["res.partner"].search([("name", "=", "Acme Widgets")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Acme Widgets",
            "is_company": True,
            "email": "info@acme.example",
        })

    # A different user we will reassign away from (so we can track change).
    other_user = env["res.users"].search([("login", "=", "demo")], limit=1)
    if not other_user:
        other_user = env["res.users"].create({
            "name": "Marc Demo",
            "login": "demo",
            "password": "demo",
            "group_ids": [(4, env.ref("base.group_user").id)],
        })

    env["crm.lead"].create({
        "name": OPP_NAME,
        "type": "opportunity",
        "partner_id": partner.id,
        "user_id": other_user.id,
        "expected_revenue": 25000.0,
    })
