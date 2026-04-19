"""Seed for mail.schedule_activity_on_partner_with_note.

Medium workflow (deep_ui_interaction): open a pre-seeded Contact, click the
chatter Activities button which opens the `mail.activity.schedule` wizard,
accept the default `To-Do` activity type, fill summary + due date + a
rich-text HTML note, and click Schedule to persist exactly one
`mail.activity` row on the partner.

Why this is medium for browser-use:
  - The wizard has multiple heterogeneous fields to fill: a many2one
    activity_type (default is `To-Do` — agents often re-pick it and leave
    it unchanged), a short summary Char, a date_deadline button-to-input
    widget (typed as US-locale `MM/DD/YYYY`), and a `note` HTML field
    rendered as an Owl wysiwyg editor (NOT a plain textarea).
  - Confusing the summary and note fields is a classic BU failure: the
    check specifically gates on both `summary == 'Follow up call'` AND
    `note` containing `Q2 plan`.

Seed responsibilities:
  - Idempotent cleanup of any lingering `Bench Activity Partner` contact,
    its chatter messages, activities, and attachments.
  - Recreate the partner fresh (is_company=True) so the task's wizard
    post registers as the sole mail.activity on the record.
"""


PARTNER_NAME = "Bench Activity Partner"
PARTNER_EMAIL = "hello@benchactivity.test"


def setup(env):
    # --- Cleanup prior runs --------------------------------------------------
    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", PARTNER_NAME),
    ])
    if partners:
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

    # --- Recreate the target partner ----------------------------------------
    env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": PARTNER_EMAIL,
        "is_company": True,
        "company_type": "company",
        "phone": "+1 555 0199",
        "street": "200 Activity Way",
        "city": "Activity City",
    })
