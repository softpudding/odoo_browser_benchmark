"""Seed opportunities for the CRM batch mark-lost wizard task.

Category 1: Closed-loop workflow.
The agent must leave the pipeline, create a new lost reason in configuration,
return to the list view, and then apply that exact reason in the batch Mark
Lost wizard.
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

    env["crm.lost.reason"].search(
        [("name", "in", ["Deferred to FY27 budget", "Deferred to next budget cycle"])]
    ).unlink()
    env["crm.lost.reason"].create({"name": "Deferred to next budget cycle"})

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
