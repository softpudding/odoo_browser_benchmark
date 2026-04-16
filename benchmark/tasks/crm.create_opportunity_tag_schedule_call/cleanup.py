"""Clean up artifacts from previous runs."""


def cleanup(env):
    leads = env["crm.lead"].search([("name", "=", "Vertex Renewal Expansion")])
    for lead in leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        lead.unlink()
