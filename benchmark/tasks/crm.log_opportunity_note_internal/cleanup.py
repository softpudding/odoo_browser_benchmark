"""Cleanup for crm.log_opportunity_note_internal.

Removes the 'Bench Note Opp' opportunity plus any chatter messages and
activities linked to it so the seed re-runs deterministically.
"""

OPP_NAME = "Bench Note Opp"


def cleanup(env):
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    if not leads:
        return
    env["mail.activity"].search([
        ("res_model", "=", "crm.lead"),
        ("res_id", "in", leads.ids),
    ]).unlink()
    env["mail.message"].search([
        ("model", "=", "crm.lead"),
        ("res_id", "in", leads.ids),
    ]).unlink()
    try:
        leads.unlink()
    except Exception:
        leads.write({"active": False})
