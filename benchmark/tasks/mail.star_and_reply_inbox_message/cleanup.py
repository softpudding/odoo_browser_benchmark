"""Cleanup for mail.star_and_reply_inbox_message."""

COORD_NAME = "Bench Coordinator"
SEEDED_SUBJECT = "Q2 status update - confirmation needed"
SEEDED_BODY = "Please confirm receipt of the Q2 status update."
REPLY_BODY = "Acknowledged - will follow up by Friday."


def cleanup(env):
    # Delete the seeded original message, any reply, and the test partner.
    env["mail.message"].search([
        "|", "|",
        ("subject", "=", SEEDED_SUBJECT),
        ("body", "ilike", SEEDED_BODY),
        ("body", "ilike", REPLY_BODY),
    ]).unlink()

    partner = env["res.partner"].search(
        [("name", "=", COORD_NAME)], limit=1
    )
    if partner:
        # Remove any lingering messages authored by this partner to avoid
        # foreign-key issues on unlink.
        env["mail.message"].search(
            [("author_id", "=", partner.id)]
        ).unlink()
        try:
            partner.unlink()
        except Exception:
            # If the partner is still referenced somewhere, archive instead.
            partner.write({"active": False})
