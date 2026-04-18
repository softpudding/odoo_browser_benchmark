"""Seed for mass_mailing.duplicate_mailing_edit_subject_send.

Seeds:
- A mailing list 'Bench Subscribers' populated with 3 contacts.
- An already-sent mailing 'Bench Newsletter V1' (state='done', sent_date set,
  Mailing List recipients, contact_list_ids empty — the agent must add
  'Bench Subscribers' to the DUPLICATE).

Capability tested: cog/Actions Duplicate on an already-sent mailing + add a
mailing list + click Send (not Schedule, not Test) on the copy, while leaving
the original untouched.
"""

from datetime import datetime


SOURCE_SUBJECT = "Bench Newsletter V1"
DUP_SUBJECT = "Bench Newsletter V2 Spring Special"
LIST_NAME = "Bench Subscribers"

CONTACT_EMAILS = [
    ("Bench Subscriber One", "sub1@bench.test"),
    ("Bench Subscriber Two", "sub2@bench.test"),
    ("Bench Subscriber Three", "sub3@bench.test"),
]


def _ensure_mass_mailing_module(env):
    module = env["ir.module.module"].search([("name", "=", "mass_mailing")], limit=1)
    if module and module.state != "installed":
        module.button_immediate_install()


def setup(env):
    _ensure_mass_mailing_module(env)

    # --- Cleanup any prior run ---
    env["mailing.mailing"].search([
        ("subject", "in", [SOURCE_SUBJECT, DUP_SUBJECT]),
    ]).unlink()
    env["mailing.contact"].search([
        ("email", "in", [e for _, e in CONTACT_EMAILS]),
    ]).unlink()
    env["mailing.list"].search([("name", "=", LIST_NAME)]).unlink()

    # --- Create mailing list + 3 contacts ---
    mailing_list = env["mailing.list"].create({"name": LIST_NAME})
    for name, email in CONTACT_EMAILS:
        env["mailing.contact"].create({
            "name": name,
            "email": email,
            "subscription_ids": [(0, 0, {
                "list_id": mailing_list.id,
                "opt_out": False,
            })],
        })

    # --- Look up the mailing.list ir.model id (required alongside mailing_model_id) ---
    list_model = env["ir.model"].search([("model", "=", "mailing.list")], limit=1)
    if not list_model:
        raise RuntimeError("ir.model for mailing.list not found")

    admin = env.ref("base.user_admin")
    email_from = admin.email or admin.partner_id.email or "admin@example.com"

    # --- Create 'Bench Newsletter V1' as an already-sent mailing ---
    # Note: we deliberately do NOT attach the Bench Subscribers list to V1.
    # The agent must explicitly add it to the duplicate. contact_list_ids stays
    # empty on the source so the duplicate also starts empty (copy_data copies
    # contact_list_ids verbatim).
    mailing_v1 = env["mailing.mailing"].create({
        "subject": SOURCE_SUBJECT,
        "email_from": email_from,
        "mailing_type": "mail",
        "mailing_model_id": list_model.id,
        "contact_list_ids": [(6, 0, [])],
        "body_html": "<p>Bench Newsletter V1 — spring edition preview.</p>",
        "body_arch": "<p>Bench Newsletter V1 — spring edition preview.</p>",
    })
    # Force the 'done' / sent state without invoking the real send pipeline
    # (the base snapshot has no outgoing mail server configured).
    mailing_v1.write({
        "state": "done",
        "sent_date": datetime(2026, 3, 15, 9, 0, 0),
        "schedule_type": "now",
    })
