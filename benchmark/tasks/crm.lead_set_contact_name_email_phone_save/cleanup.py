"""Clean up artifacts from previous runs of
crm.lead_set_contact_name_email_phone_save."""

LEAD_NAME = "Bench Lead Basic"


def cleanup(env):
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", LEAD_NAME),
    ])
    if leads:
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        leads.unlink()
