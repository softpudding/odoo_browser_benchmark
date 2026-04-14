"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Redwood Consulting")], limit=1)
    if partner:
        invoices = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("ref", "=", "SURG-EDIT-01"),
        ])
        for inv in invoices:
            if inv.state == "posted":
                inv.button_draft()
            if inv.state == "draft":
                inv.button_cancel()
            inv.unlink()
