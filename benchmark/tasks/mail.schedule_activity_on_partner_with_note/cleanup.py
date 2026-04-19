"""Cleanup for mail.schedule_activity_on_partner_with_note.

Removes the 'Bench Activity Partner' contact plus any activities, chatter
messages, and ir.attachment rows linked to it so the seed re-runs
deterministically.
"""


PARTNER_NAME = "Bench Activity Partner"


def cleanup(env):
    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", PARTNER_NAME),
    ])
    if not partners:
        return
    env["mail.activity"].search([
        ("res_model", "=", "res.partner"),
        ("res_id", "in", partners.ids),
    ]).unlink()
    env["mail.message"].search([
        ("model", "=", "res.partner"),
        ("res_id", "in", partners.ids),
    ]).unlink()
    env["ir.attachment"].search([
        ("res_model", "=", "res.partner"),
        ("res_id", "in", partners.ids),
    ]).unlink()
    try:
        partners.unlink()
    except Exception:
        partners.write({"active": False})
