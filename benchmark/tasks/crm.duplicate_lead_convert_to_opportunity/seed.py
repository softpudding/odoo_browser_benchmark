"""Seed for crm.duplicate_lead_convert_to_opportunity.

Medium workflow. Requires the admin to have the `crm.group_use_lead` group so
the Leads submenu and the Convert-to-Opportunity button exist. Seeds one
template lead (`Bench Template Lead`, type='lead') for the agent to clone.

We pre-clear any prior cloned-opp records and any prior test partner so re-runs
start from a clean slate.
"""

TEMPLATE_LEAD_NAME = "Bench Template Lead"
CLONED_LEAD_NAME = "Bench Cloned Opp"
CLONED_COPY_AUTO_NAME = "Bench Template Lead (copy)"
NEW_PARTNER_NAME = "Bench Cloned Customer"


def setup(env):
    # --- Ensure admin has the Leads feature enabled ---
    group_lead = env.ref("crm.group_use_lead", raise_if_not_found=False)
    if group_lead:
        admin = env.ref("base.user_admin")
        if group_lead not in admin.group_ids:
            admin.write({"group_ids": [(4, group_lead.id)]})

    # --- Cleanup prior runs ---
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
    stale_partners = Partner.search([("name", "=", NEW_PARTNER_NAME)])
    stale_partners.unlink()

    # --- Seed the template lead (type='lead') ---
    Lead.create({
        "name": TEMPLATE_LEAD_NAME,
        "type": "lead",
        "description": "<p>Inbound qualification template — clone for new prospects.</p>",
        "contact_name": "Template Contact",
        "email_from": "template.bench@example.com",
        "expected_revenue": 1500.0,
    })
