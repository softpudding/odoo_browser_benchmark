"""Cleanup for crm.duplicate_lead_convert_to_opportunity."""

TEMPLATE_LEAD_NAME = "Bench Template Lead"
CLONED_LEAD_NAME = "Bench Cloned Opp"
CLONED_COPY_AUTO_NAME = "Bench Template Lead (copy)"
NEW_PARTNER_NAME = "Bench Cloned Customer"


def cleanup(env):
    Lead = env["crm.lead"].with_context(active_test=False)
    stale_names = [
        TEMPLATE_LEAD_NAME,
        CLONED_LEAD_NAME,
        CLONED_COPY_AUTO_NAME,
    ]
    stale_leads = Lead.search([("name", "in", stale_names)])
    for lead in stale_leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
    stale_leads.unlink()

    Partner = env["res.partner"].with_context(active_test=False)
    Partner.search([("name", "=", NEW_PARTNER_NAME)]).unlink()
