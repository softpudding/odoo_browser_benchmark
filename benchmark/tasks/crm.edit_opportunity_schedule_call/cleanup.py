"""Clean up artifacts from previous runs."""

TARGET_NAME = "Beacon Analytics Deal"


def cleanup(env):
    leads = env["crm.lead"].search([("name", "=", TARGET_NAME)])
    for lead in leads:
        activities = env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ])
        activities.unlink()
        lead.unlink()
