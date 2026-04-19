"""Clean up artifacts from previous runs of crm.assign_lead_salesperson_change_stage_won."""

OPP_NAME = "Bench Big Deal"


def cleanup(env):
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
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
