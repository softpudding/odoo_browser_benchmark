"""Cleanup for crm.assign_team_change_salesperson_log_activity."""


def cleanup(env):
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", "Bench Big Deal"),
    ])
    for lead in leads:
        acts = env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ])
        acts.unlink()
    leads.unlink()
