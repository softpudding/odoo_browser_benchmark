"""Seed a CRM lead and partner for the lead-conversion task.

Category 2 (MEDIUM): The agent must convert a specific lead to an
opportunity, linking to an existing customer via the conversion wizard.
Capability tested: Lead conversion wizard, non-default link-to-existing
choice, without touching sibling records.
"""


def setup(env):
    # --- Enable the Leads feature in CRM settings ---
    group_lead = env.ref("crm.group_use_lead", raise_if_not_found=False)
    if group_lead:
        admin = env.ref("base.user_admin")
        if group_lead not in admin.group_ids:
            admin.write({"group_ids": [(4, group_lead.id)]})

    # --- Ensure customer ---
    partner = env["res.partner"].search(
        [("name", "=", "Spark Innovations")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Spark Innovations",
            "email": "hello@sparkinnovations.com",
            "is_company": True,
        })

    # --- Cleanup prior runs ---
    old = env["crm.lead"].search([
        ("name", "in", [
            "Spark Innovations - Pager SaaS",
            "Riverstone Retail - Fitting Line",
        ]),
    ])
    old.unlink()

    # --- Create the target lead ---
    env["crm.lead"].create({
        "name": "Spark Innovations - Pager SaaS",
        "type": "lead",
        "contact_name": "Morgan Clarke",
        "email_from": "morgan@sparkinnovations.com",
        "phone": "+1 415 555 0142",
        "description": (
            "Spark Innovations wants to replace their legacy pager rotation "
            "with a SaaS dashboard. Budget approved for Q3."
        ),
        "expected_revenue": 18000.0,
    })

    # --- Distractor lead (similar-sounding but unrelated) ---
    env["crm.lead"].create({
        "name": "Riverstone Retail - Fitting Line",
        "type": "lead",
        "contact_name": "Avery Duke",
        "email_from": "avery@riverstoneretail.com",
        "expected_revenue": 8000.0,
    })
