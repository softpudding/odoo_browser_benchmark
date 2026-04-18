"""Cleanup for mass_mailing.create_segmented_mailing_save_draft."""


SUBJECT = "Berlin April Bulletin"
PARTNER_NAMES = ["Berlin Alpha Co", "Berlin Beta Co", "Munich Gamma Co"]


def cleanup(env):
    env["mailing.mailing"].search([("subject", "=", SUBJECT)]).unlink()
    for name in PARTNER_NAMES:
        partners = env["res.partner"].sudo().search([
            ("name", "=", name),
            ("is_company", "=", True),
        ])
        for partner in partners:
            try:
                partner.unlink()
            except Exception:
                # Leave behind partners referenced by other records.
                pass
