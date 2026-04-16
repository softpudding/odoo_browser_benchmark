"""Seed an opportunity for the update-opportunity-revenue task."""

OPP_NAME = "BENCH-OPP-REV-01"
PARTNER_NAME = "Northstar Ventures"


def setup(env):
    env["crm.lead"].search([("name", "=", OPP_NAME)]).unlink()

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": PARTNER_NAME})

    team = env["crm.team"].search([], limit=1)
    team_id = team.id if team else False

    env["crm.lead"].create({
        "name": OPP_NAME,
        "partner_id": partner.id,
        "type": "opportunity",
        "expected_revenue": 5000.0,
        "user_id": env.ref("base.user_admin").id,
        "team_id": team_id,
    })
