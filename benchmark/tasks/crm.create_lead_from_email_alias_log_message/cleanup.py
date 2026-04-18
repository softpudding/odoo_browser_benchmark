"""Cleanup for crm.create_lead_from_email_alias_log_message."""

LEAD_NAME = "Inbound Inquiry from Sample"
TEAM_NAME = "Inbound"


def cleanup(env):
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", LEAD_NAME),
    ])
    for lead in leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
    leads.unlink()

    # Reset the team's alias so re-runs start from a known state.
    team = env["crm.team"].with_context(active_test=False).search([
        ("name", "=", TEAM_NAME),
    ], limit=1)
    if team and team.alias_name:
        team.write({"alias_name": False})
