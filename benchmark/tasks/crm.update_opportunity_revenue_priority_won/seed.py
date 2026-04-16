"""Seed opportunities for the update-opportunity-revenue-priority-won task.

Category 2 (MEDIUM): open the correct opportunity, edit revenue, use the star
priority widget, then trigger the explicit Won action while leaving a similar
distractor untouched.
"""

TARGET_NAME = "Northwind Renewal Review"
DISTRACTOR_NAME = "Northwind Renewal Pilot"


def setup(env):
    lead_env = env["crm.lead"].with_context(active_test=False)
    old = lead_env.search([("name", "in", [TARGET_NAME, DISTRACTOR_NAME])])
    if old:
        old.unlink()

    admin = env.ref("base.user_admin")
    team = env["crm.team"].search([], limit=1)

    specs = [
        (TARGET_NAME, "Northwind Retail", "renewal@northwind.example.com", 16500.0, "1"),
        (DISTRACTOR_NAME, "Northwind Retail", "pilot@northwind.example.com", 9200.0, "0"),
    ]
    for name, partner_name, email, revenue, priority in specs:
        env["crm.lead"].create({
            "name": name,
            "partner_name": partner_name,
            "email_from": email,
            "type": "opportunity",
            "expected_revenue": revenue,
            "priority": priority,
            "user_id": admin.id,
            "team_id": team.id if team else False,
        })
