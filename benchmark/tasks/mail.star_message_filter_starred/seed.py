"""Seed for mail.star_message_filter_starred.

Creates three inbox messages for the admin partner; the task is to star
the specific one referencing Q2 cutoff.
"""

TARGET_SUBJECT = "Finance close blocker — action required for Q2 cutoff"
DISTRACTOR_SUBJECTS = [
    "Office WiFi upgrade – FYI",
    "Welcome lunch sign-up",
]


def setup(env):
    admin = env.ref("base.user_admin")

    # Ensure a distinct author user exists (OdooBot or demo) to post from.
    author = env["res.users"].search([("login", "=", "marc.demo")], limit=1)
    if not author:
        author = env["res.users"].create({
            "name": "Marc Demo",
            "login": "marc.demo",
            "email": "marc.demo@example.com",
            "group_ids": [(6, 0, [env.ref("base.group_user").id])],
        })

    # Remove prior instances of our test messages.
    for subj in [TARGET_SUBJECT] + DISTRACTOR_SUBJECTS:
        env["mail.message"].search([("subject", "=", subj)]).unlink()

    # Post messages from Marc Demo addressed to admin — creates
    # needaction notifications that land in admin's Inbox.
    for subj in DISTRACTOR_SUBJECTS + [TARGET_SUBJECT]:
        admin.partner_id.with_user(author).message_post(
            body=f"<p>{subj}</p>",
            subject=subj,
            message_type="comment",
            subtype_xmlid="mail.mt_comment",
            partner_ids=[admin.partner_id.id],
        )

    # Clear any prior starred flag on these messages for a clean start.
    msgs = env["mail.message"].search([
        ("subject", "in", [TARGET_SUBJECT] + DISTRACTOR_SUBJECTS),
    ])
    for m in msgs:
        if admin.partner_id in m.starred_partner_ids:
            m.write({"starred_partner_ids": [(3, admin.partner_id.id)]})
