"""Cleanup for crm_iap_enrich.bulk_enrich_leads_from_list."""

NAMES = [
    "Bench Enrich Target Alpha",
    "Bench Enrich Target Bravo",
    "Bench Enrich Target Charlie",
    "Bench Enrich Already Delta",
    "Bench Enrich Manual Echo",
]


def cleanup(env):
    Lead = env["crm.lead"].with_context(active_test=False)
    stale = Lead.search([("name", "in", NAMES)])
    for lead in stale:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
    stale.unlink()
