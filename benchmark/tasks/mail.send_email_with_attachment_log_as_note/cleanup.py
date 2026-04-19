"""Cleanup for mail.send_email_with_attachment_log_as_note.

Removes the 'Bench Chatter Co' partner plus any chatter messages,
activities, and ir.attachment rows linked to it so the seed re-runs
deterministically.
"""


PARTNER_NAME = "Bench Chatter Co"
ATTACHMENT_FILENAME = "welcome_kit.txt"


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
    # Belt-and-suspenders: drop any orphan welcome_kit.txt attachments
    # linked to res.partner but whose parent partner is gone.
    env["ir.attachment"].with_context(active_test=False).search([
        ("name", "=", ATTACHMENT_FILENAME),
        ("res_model", "=", "res.partner"),
    ]).unlink()
