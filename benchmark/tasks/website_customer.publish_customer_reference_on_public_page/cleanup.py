"""Cleanup for website_customer.publish_customer_reference_on_public_page."""

CLIENT_NAME = "Bench Happy Client"
IMPLEMENTER_NAME = "Bench Delivery Partner"


def cleanup(env):
    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "in", [CLIENT_NAME, IMPLEMENTER_NAME]),
    ])
    if partners:
        # Null back-refs before unlink.
        referring = env["res.partner"].with_context(active_test=False).search([
            ("assigned_partner_id", "in", partners.ids),
        ])
        if referring:
            referring.sudo().write({"assigned_partner_id": False})
        try:
            partners.sudo().unlink()
        except Exception:
            partners.sudo().write({"active": False})
