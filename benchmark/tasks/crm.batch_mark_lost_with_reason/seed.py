"""Seed opportunities for the CRM batch mark-lost wizard task.

Category 2: Policy trap (wizard).
The agent must leave the default kanban view, switch to list view, select the
correct pair of rows, and complete the Mark Lost wizard with an explicit loss
reason and closing note. Browser-use often mis-selects rows or skips the note.
"""


def setup(env):
    lead_env = env["crm.lead"].with_context(active_test=False)
    old = lead_env.search(
        [
            (
                "name",
                "in",
                [
                    "Blue Canyon Power Renewal",
                    "Blue Canyon Power Expansion",
                    "Blue Canyon Logistics Renewal",
                ],
            )
        ]
    )
    if old:
        old.unlink()

    reason = env["crm.lost.reason"].search([("name", "=", "Price too high")], limit=1)
    if not reason:
        env["crm.lost.reason"].create({"name": "Price too high"})

    admin = env.ref("base.user_admin")
    team = env["crm.team"].search([], limit=1)

    specs = [
        ("Blue Canyon Power Renewal", "Blue Canyon Power", "renewal@bluecanyon.example.com", 18000.0),
        ("Blue Canyon Power Expansion", "Blue Canyon Power", "renewal@bluecanyon.example.com", 24000.0),
        ("Blue Canyon Logistics Renewal", "Blue Canyon Logistics", "renewal@bluecanyon-logistics.example.com", 21000.0),
    ]
    for name, partner_name, email, revenue in specs:
        env["crm.lead"].create(
            {
                "name": name,
                "partner_name": partner_name,
                "email_from": email,
                "type": "opportunity",
                "expected_revenue": revenue,
                "user_id": admin.id,
                "team_id": team.id if team else False,
            }
        )
